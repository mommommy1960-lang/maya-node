"""
RSOM Binding Hooks
Runtime Service Orchestration Model binding hooks for CUP
"""

from typing import Any, Callable, Dict, List, Optional
import logging


logger = logging.getLogger(__name__)


class RsomBindingHooks:
    """RSOM binding hooks for runtime orchestration"""
    
    def __init__(self):
        self._pre_hooks: Dict[str, List[Callable]] = {}
        self._post_hooks: Dict[str, List[Callable]] = {}
        self._error_hooks: Dict[str, List[Callable]] = {}
    
    def register_pre_hook(self, event_name: str, hook: Callable):
        """Register a pre-execution hook
        
        Args:
            event_name: Name of the event to hook
            hook: Callable to execute before the event
        """
        if event_name not in self._pre_hooks:
            self._pre_hooks[event_name] = []
        self._pre_hooks[event_name].append(hook)
        logger.info(f"Registered pre-hook for event: {event_name}")
    
    def register_post_hook(self, event_name: str, hook: Callable):
        """Register a post-execution hook
        
        Args:
            event_name: Name of the event to hook
            hook: Callable to execute after the event
        """
        if event_name not in self._post_hooks:
            self._post_hooks[event_name] = []
        self._post_hooks[event_name].append(hook)
        logger.info(f"Registered post-hook for event: {event_name}")
    
    def register_error_hook(self, event_name: str, hook: Callable):
        """Register an error handling hook
        
        Args:
            event_name: Name of the event to hook
            hook: Callable to execute on error
        """
        if event_name not in self._error_hooks:
            self._error_hooks[event_name] = []
        self._error_hooks[event_name].append(hook)
        logger.info(f"Registered error-hook for event: {event_name}")
    
    def execute_pre_hooks(self, event_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute pre-hooks for an event
        
        Args:
            event_name: Name of the event
            context: Context data for the hooks
            
        Returns:
            Modified context after hook execution
        """
        if event_name in self._pre_hooks:
            for hook in self._pre_hooks[event_name]:
                try:
                    context = hook(context) or context
                except Exception as e:
                    logger.error(f"Error executing pre-hook for {event_name}: {e}")
                    self._handle_error(event_name, e, context)
        return context
    
    def execute_post_hooks(self, event_name: str, context: Dict[str, Any], result: Any) -> Any:
        """Execute post-hooks for an event
        
        Args:
            event_name: Name of the event
            context: Context data for the hooks
            result: Result from the event execution
            
        Returns:
            Modified result after hook execution
        """
        if event_name in self._post_hooks:
            for hook in self._post_hooks[event_name]:
                try:
                    result = hook(context, result) or result
                except Exception as e:
                    logger.error(f"Error executing post-hook for {event_name}: {e}")
                    self._handle_error(event_name, e, context)
        return result
    
    def _handle_error(self, event_name: str, error: Exception, context: Dict[str, Any]):
        """Handle errors in hook execution
        
        Args:
            event_name: Name of the event
            error: Exception that occurred
            context: Context data
        """
        if event_name in self._error_hooks:
            for hook in self._error_hooks[event_name]:
                try:
                    hook(error, context)
                except Exception as e:
                    logger.error(f"Error in error-hook for {event_name}: {e}")
    
    def clear_hooks(self, event_name: Optional[str] = None):
        """Clear hooks for a specific event or all events
        
        Args:
            event_name: Optional event name. If None, clears all hooks.
        """
        if event_name:
            self._pre_hooks.pop(event_name, None)
            self._post_hooks.pop(event_name, None)
            self._error_hooks.pop(event_name, None)
            logger.info(f"Cleared hooks for event: {event_name}")
        else:
            self._pre_hooks.clear()
            self._post_hooks.clear()
            self._error_hooks.clear()
            logger.info("Cleared all hooks")


# Global instance for convenience
_global_hooks = RsomBindingHooks()


def get_hooks() -> RsomBindingHooks:
    """Get the global RSOM binding hooks instance"""
    return _global_hooks
