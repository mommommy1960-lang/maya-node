"""Fail-closed human approval gate. Notification delivery and staffing are integration duties."""
from __future__ import annotations
import copy, threading, time, uuid
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

class ApprovalStatus(str, Enum):
    PENDING="pending"; APPROVED="approved"; REJECTED="rejected"
    TIMEOUT="timeout"; CANCELLED="cancelled"

@dataclass
class ApprovalRequest:
    request_id: str
    operation: str
    context: Dict[str, Any]
    sensitivity_level: str
    timestamp: float
    expires_at: float
    status: ApprovalStatus=ApprovalStatus.PENDING
    approver: Optional[str]=None
    decision_notes: Optional[str]=None
    decided_at: Optional[float]=None

class ApprovalGate:
    """Thread-safe, fail-closed manual approval state machine.

    A real deployment must provide authenticated approver_authorizer and a
    durable audit_sink. No notifications or staffed coverage are implied.
    """
    LEVELS={"low","medium","high","critical"}
    def __init__(self, approver_authorizer: Optional[Callable]=None,
                 audit_sink: Optional[Callable]=None, clock: Callable=time.time):
        self.authorizer=approver_authorizer; self.audit_sink=audit_sink
        self.clock=clock; self.pending={}; self.history=[]; self.halted=False
        self.lock=threading.RLock()

    def _event(self, event):
        item=copy.deepcopy(event)
        if self.audit_sink: self.audit_sink(copy.deepcopy(item))
        self.history.append(item)

    def request(self, operation, context, sensitivity="high", ttl=300):
        if not isinstance(operation,str) or not operation.strip(): raise ValueError("operation required")
        if sensitivity not in self.LEVELS: raise ValueError("invalid sensitivity")
        if isinstance(ttl,bool) or not isinstance(ttl,(int,float)) or ttl<=0: raise ValueError("ttl must be positive")
        now=self.clock()
        r=ApprovalRequest("apr_"+uuid.uuid4().hex,operation,copy.deepcopy(context),sensitivity,now,now+ttl)
        with self.lock:
            if self.halted:
                r.status=ApprovalStatus.CANCELLED; r.decision_notes="system halted"
                return r
            self.pending[r.request_id]=r
            self._event({"event":"requested","id":r.request_id,"operation":operation,"at":now,"expires":r.expires_at})
        return copy.deepcopy(r)

    def _decide(self, request_id, actor, status, notes):
        if not actor or not isinstance(actor,str): raise ValueError("authenticated actor required")
        with self.lock:
            r=self.pending.get(request_id)
            if r is None: return False
            now=self.clock()
            if now>=r.expires_at:
                r.status=ApprovalStatus.TIMEOUT; r.decided_at=now; self.pending.pop(request_id)
                self._event({"event":"timeout","id":request_id,"at":now}); return False
            if self.authorizer is None or not self.authorizer(actor,copy.deepcopy(r)):
                raise PermissionError("no configured authorization for this approver")
            self._event({"event":"decision","id":request_id,"status":status.value,"actor":actor,"notes":notes,"at":now})
            r.status=status; r.approver=actor; r.decision_notes=notes; r.decided_at=now
            self.pending.pop(request_id); return True

    def approve(self, request_id, actor, notes=""):
        return self._decide(request_id,actor,ApprovalStatus.APPROVED,notes)
    def reject(self, request_id, actor, reason):
        if not reason or not reason.strip(): raise ValueError("rejection reason required")
        return self._decide(request_id,actor,ApprovalStatus.REJECTED,reason)
    def expire(self):
        now=self.clock(); count=0
        with self.lock:
            for key,r in list(self.pending.items()):
                if now>=r.expires_at:
                    r.status=ApprovalStatus.TIMEOUT; r.decided_at=now; self.pending.pop(key)
                    self._event({"event":"timeout","id":key,"at":now}); count+=1
        return count
    def cancel(self, request_id, actor, reason):
        if not actor or not reason: raise ValueError("actor and reason required")
        with self.lock:
            r=self.pending.pop(request_id,None)
            if r is None: return False
            r.status=ApprovalStatus.CANCELLED; r.approver=actor; r.decision_notes=reason; r.decided_at=self.clock()
            self._event({"event":"cancelled","id":request_id,"actor":actor,"reason":reason,"at":r.decided_at})
            return True
    def override(self, actor, reason):
        if not actor or not reason: raise ValueError("actor and reason required")
        with self.lock:
            self.halted=True; now=self.clock()
            for r in self.pending.values():
                r.status=ApprovalStatus.CANCELLED; r.decision_notes="cancelled by override"; r.decided_at=now
            self.pending.clear(); self._event({"event":"override","actor":actor,"reason":reason,"at":now})
    def resume(self, actor, authorized=False):
        if not authorized or not actor: raise PermissionError("authorized human required")
        with self.lock:
            self._event({"event":"resume","actor":actor,"at":self.clock()}); self.halted=False
    def pending_requests(self):
        self.expire()
        with self.lock: return copy.deepcopy(list(self.pending.values()))
    def history_snapshot(self):
        with self.lock: return copy.deepcopy(self.history)
