# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Human-in-the-Loop (HITL) Interface

This module implements human oversight and control mechanisms to ensure
human autonomy and final decision-making authority.

Key Features:
- Human approval workflows
- Override mechanisms
- Feedback collection
- Escalation paths
- Audit trail of human decisions
"""

import logging
from typing import Any, Dict, Optional, Callable, List
from dataclasses import dataclass
from enum import Enum
import time

logger = logging.getLogger(__name__)


class ApprovalStatus(Enum):
    """Status of human approval requests"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    TIMEOUT = "timeout"


@dataclass
class ApprovalRequest:
    """Represents a request for human approval"""
    request_id: str
    operation: str
    context: Dict[str, Any]
    sensitivity_level: str
    timestamp: float
    status: ApprovalStatus = ApprovalStatus.PENDING
    approver: Optional[str] = None
    decision_notes: Optional[str] = None


class HumanInTheLoop:
    """
    Human-in-the-loop interface for AI oversight.
    
    Ensures humans maintain control over AI operations:
    - Approval for sensitive operations
    - Override capability at any time
    - Feedback and correction mechanisms
    - Transparent decision history
    """
    
    def __init__(self, auto_approve_dev: bool = False):
        """
        Initialize HITL interface.
        
        Args:
            auto_approve_dev: Auto-approve in development mode (for testing)
        """
        logger.info("Initializing Human-in-the-Loop Interface")
        
        self.auto_approve_dev = auto_approve_dev
        self.pending_requests: Dict[str, ApprovalRequest] = {}
        self.decision_history = []
        self.override_callbacks: List[Callable] = []
        
        if auto_approve_dev:
            logger.warning("HITL in auto-approve mode (DEVELOPMENT ONLY)")
        
        logger.info("HITL Interface ready")
    
    def request_approval(
        self,
        operation: str,
        context: Dict[str, Any],
        sensitivity_level: str = "medium",
        timeout_seconds: float = 300.0
    ) -> ApprovalRequest:
        """
        Request human approval for an operation.
        
        Args:
            operation: Description of operation requiring approval
            context: Context information for decision
            sensitivity_level: Sensitivity level (low/medium/high/critical)
            timeout_seconds: How long to wait for approval
            
        Returns:
            ApprovalRequest object with status
        """
        request_id = f"approval_{int(time.time())}_{len(self.pending_requests)}"
        
        request = ApprovalRequest(
            request_id=request_id,
            operation=operation,
            context=context,
            sensitivity_level=sensitivity_level,
            timestamp=time.time()
        )
        
        self.pending_requests[request_id] = request
        
        logger.info(
            f"Approval requested: {operation} "
            f"(sensitivity: {sensitivity_level}, id: {request_id})"
        )
        
        # In development mode, auto-approve
        if self.auto_approve_dev:
            request.status = ApprovalStatus.APPROVED
            request.approver = "auto_dev"
            request.decision_notes = "Auto-approved in development mode"
            self.decision_history.append(request)
            logger.info(f"Auto-approved: {request_id}")
        else:
            # TODO: Implement actual approval mechanism
            # - Send notification to human operator
            # - Wait for response or timeout
            # - Handle approval/rejection
            logger.warning(
                f"HITL approval required but not implemented. "
                f"Request {request_id} pending."
            )
        
        return request
    
    def approve(
        self,
        request_id: str,
        approver: str,
        notes: Optional[str] = None
    ) -> bool:
        """
        Approve a pending request.
        
        Args:
            request_id: ID of request to approve
            approver: Identifier of approving human
            notes: Optional decision notes
            
        Returns:
            True if approved successfully
        """
        if request_id not in self.pending_requests:
            logger.error(f"Request {request_id} not found")
            return False
        
        request = self.pending_requests[request_id]
        request.status = ApprovalStatus.APPROVED
        request.approver = approver
        request.decision_notes = notes
        
        self.decision_history.append(request)
        del self.pending_requests[request_id]
        
        logger.info(f"Request approved: {request_id} by {approver}")
        return True
    
    def reject(
        self,
        request_id: str,
        approver: str,
        reason: str
    ) -> bool:
        """
        Reject a pending request.
        
        Args:
            request_id: ID of request to reject
            approver: Identifier of rejecting human
            reason: Reason for rejection
            
        Returns:
            True if rejected successfully
        """
        if request_id not in self.pending_requests:
            logger.error(f"Request {request_id} not found")
            return False
        
        request = self.pending_requests[request_id]
        request.status = ApprovalStatus.REJECTED
        request.approver = approver
        request.decision_notes = f"Rejected: {reason}"
        
        self.decision_history.append(request)
        del self.pending_requests[request_id]
        
        logger.warning(f"Request rejected: {request_id} by {approver}")
        return True
    
    def override(self, reason: str, callback: Optional[Callable] = None) -> None:
        """
        Immediate human override to halt operations.
        
        Args:
            reason: Reason for override
            callback: Optional callback to execute on override
        """
        logger.critical(f"HUMAN OVERRIDE ACTIVATED: {reason}")
        
        # Execute registered callbacks
        for cb in self.override_callbacks:
            try:
                cb(reason)
            except Exception as e:
                logger.error(f"Override callback error: {e}")
        
        if callback:
            callback(reason)
        
        # Log to decision history
        self.decision_history.append({
            "type": "override",
            "reason": reason,
            "timestamp": time.time()
        })
    
    def register_override_callback(self, callback: Callable) -> None:
        """
        Register a callback to be executed on override.
        
        Args:
            callback: Function to call on override
        """
        self.override_callbacks.append(callback)
        logger.info("Override callback registered")
    
    def collect_feedback(
        self,
        operation_id: str,
        feedback: str,
        rating: Optional[int] = None
    ) -> None:
        """
        Collect human feedback on an operation.
        
        Args:
            operation_id: ID of operation to provide feedback on
            feedback: Feedback text
            rating: Optional numerical rating (1-5)
        """
        feedback_entry = {
            "operation_id": operation_id,
            "feedback": feedback,
            "rating": rating,
            "timestamp": time.time()
        }
        
        self.decision_history.append(feedback_entry)
        logger.info(f"Feedback collected for {operation_id}")
    
    def get_pending_requests(self) -> List[ApprovalRequest]:
        """
        Get all pending approval requests.
        
        Returns:
            List of pending requests
        """
        return list(self.pending_requests.values())
    
    def get_decision_history(self) -> List[Any]:
        """
        Get complete decision history.
        
        Returns:
            List of all decisions and feedback
        """
        return self.decision_history.copy()


def main():
    """Example usage of the HITL interface."""
    
    # Development mode with auto-approve
    hitl = HumanInTheLoop(auto_approve_dev=True)
    
    # Request approval
    request = hitl.request_approval(
        operation="adjust_energy_distribution",
        context={"load": "high", "battery_soc": 0.3},
        sensitivity_level="medium"
    )
    
    print(f"Request status: {request.status}")
    print(f"Approver: {request.approver}")
    
    # Collect feedback
    hitl.collect_feedback(
        operation_id="op_123",
        feedback="Operation completed successfully",
        rating=5
    )
    
    print(f"\nDecision history entries: {len(hitl.get_decision_history())}")


if __name__ == "__main__":
    main()
