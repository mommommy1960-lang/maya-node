"""
Signal Classifier

Classifies market signals based on type, urgency, and confidence level.
"""

from enum import Enum
from typing import Dict, Any, Optional


class SignalType(Enum):
    """Types of market signals."""
    PRICE = "price"
    DEMAND = "demand"
    SUPPLY = "supply"
    REGULATORY = "regulatory"
    WEATHER = "weather"
    NEWS = "news"
    ANOMALY = "anomaly"


class SignalUrgency(Enum):
    """Signal urgency levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class SignalClassifier:
    """
    Classifies market signals for prioritization and routing.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the signal classifier.
        
        Args:
            config: Optional configuration for classification rules
        """
        self.config = config or {}
        self.classification_rules = self._load_rules()
        
    def _load_rules(self) -> Dict[str, Any]:
        """Load classification rules from configuration."""
        return {
            "price_threshold_high": 0.15,  # 15% change
            "price_threshold_critical": 0.30,  # 30% change
            "confidence_minimum": 0.6,
        }
        
    def classify(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify a market signal.
        
        Args:
            signal: Raw signal data
            
        Returns:
            Classified signal with type, urgency, and confidence
        """
        signal_type = self._determine_type(signal)
        urgency = self._determine_urgency(signal, signal_type)
        confidence = self._calculate_confidence(signal)
        
        return {
            "original": signal,
            "type": signal_type.value,
            "urgency": urgency.value,
            "confidence": confidence,
            "timestamp": signal.get("timestamp"),
        }
        
    def _determine_type(self, signal: Dict[str, Any]) -> SignalType:
        """Determine the type of signal."""
        # Placeholder logic - to be implemented based on signal structure
        if "price" in signal:
            return SignalType.PRICE
        elif "demand" in signal:
            return SignalType.DEMAND
        elif "weather" in signal:
            return SignalType.WEATHER
        else:
            return SignalType.NEWS
            
    def _determine_urgency(
        self, signal: Dict[str, Any], signal_type: SignalType
    ) -> SignalUrgency:
        """Determine the urgency level of a signal."""
        # Placeholder logic - to be implemented
        if signal_type == SignalType.PRICE:
            change = signal.get("change_percent", 0)
            if abs(change) >= self.classification_rules["price_threshold_critical"]:
                return SignalUrgency.CRITICAL
            elif abs(change) >= self.classification_rules["price_threshold_high"]:
                return SignalUrgency.HIGH
        return SignalUrgency.MEDIUM
        
    def _calculate_confidence(self, signal: Dict[str, Any]) -> float:
        """Calculate confidence score for a signal."""
        # Placeholder logic - to be implemented
        return signal.get("confidence", 0.8)
        
    def batch_classify(self, signals: list) -> list:
        """
        Classify multiple signals.
        
        Args:
            signals: List of raw signals
            
        Returns:
            List of classified signals
        """
        return [self.classify(signal) for signal in signals]


if __name__ == "__main__":
    classifier = SignalClassifier()
    test_signal = {"price": 100, "change_percent": 0.20, "timestamp": "2025-11-10"}
    result = classifier.classify(test_signal)
    print(f"Classified signal: {result}")
