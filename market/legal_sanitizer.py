"""
Legal Sanitizer

Ensures market intelligence data and reports comply with legal and regulatory
requirements by sanitizing sensitive information and ensuring proper disclosures.
"""

import re
from typing import Dict, Any, List, Optional
from enum import Enum


class SensitivityLevel(Enum):
    """Data sensitivity classification levels."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class LegalSanitizer:
    """
    Sanitizes market intelligence data for legal compliance.
    
    Handles removal of personally identifiable information (PII),
    insider information, and other legally sensitive data.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the legal sanitizer.
        
        Args:
            config: Optional configuration for sanitization rules
        """
        self.config = config or {}
        self.patterns = self._load_patterns()
        self.compliance_rules = self._load_compliance_rules()
        
    def _load_patterns(self) -> Dict[str, re.Pattern]:
        """Load regex patterns for identifying sensitive data."""
        return {
            "email": re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            "phone": re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            "ssn": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            "credit_card": re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),
            "api_key": re.compile(r'\b[A-Za-z0-9]{32,}\b'),
        }
        
    def _load_compliance_rules(self) -> Dict[str, Any]:
        """Load compliance rules and requirements."""
        return {
            "require_disclaimers": True,
            "anonymize_sources": True,
            "redact_insider_info": True,
            "mask_personal_data": True,
        }
        
    def sanitize_text(self, text: str, level: SensitivityLevel = SensitivityLevel.PUBLIC) -> str:
        """
        Sanitize text content based on sensitivity level.
        
        Args:
            text: Text to sanitize
            level: Target sensitivity level
            
        Returns:
            Sanitized text
        """
        sanitized = text
        
        # Redact PII
        if level in [SensitivityLevel.PUBLIC, SensitivityLevel.INTERNAL]:
            sanitized = self._redact_pii(sanitized)
            
        # Remove sensitive patterns
        for pattern_name, pattern in self.patterns.items():
            sanitized = pattern.sub(f"[REDACTED-{pattern_name.upper()}]", sanitized)
            
        return sanitized
        
    def _redact_pii(self, text: str) -> str:
        """Redact personally identifiable information."""
        # Remove email addresses
        text = self.patterns["email"].sub("[REDACTED-EMAIL]", text)
        # Remove phone numbers
        text = self.patterns["phone"].sub("[REDACTED-PHONE]", text)
        # Remove SSN
        text = self.patterns["ssn"].sub("[REDACTED-SSN]", text)
        return text
        
    def sanitize_report(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize a complete market intelligence report.
        
        Args:
            report: Report data dictionary
            
        Returns:
            Sanitized report
        """
        sanitized_report = report.copy()
        
        # Sanitize text fields
        for key, value in sanitized_report.items():
            if isinstance(value, str):
                sanitized_report[key] = self.sanitize_text(value)
            elif isinstance(value, dict):
                sanitized_report[key] = self.sanitize_report(value)
            elif isinstance(value, list):
                sanitized_report[key] = [
                    self.sanitize_text(item) if isinstance(item, str)
                    else self.sanitize_report(item) if isinstance(item, dict)
                    else item
                    for item in value
                ]
                
        # Add required disclaimers
        if self.compliance_rules["require_disclaimers"]:
            sanitized_report["legal_disclaimer"] = self._get_disclaimer()
            
        return sanitized_report
        
    def _get_disclaimer(self) -> str:
        """Generate legal disclaimer text."""
        return (
            "This report is provided for informational purposes only. "
            "It does not constitute financial, legal, or investment advice. "
            "All data is anonymized and aggregated to protect confidentiality. "
            "Users should conduct their own due diligence and consult with "
            "qualified professionals before making decisions based on this information."
        )
        
    def validate_compliance(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate that data meets compliance requirements.
        
        Args:
            data: Data to validate
            
        Returns:
            Tuple of (is_compliant, list of issues)
        """
        issues = []
        
        # Check for unsanitized PII
        data_str = str(data)
        for pattern_name, pattern in self.patterns.items():
            if pattern.search(data_str):
                issues.append(f"Unsanitized {pattern_name} detected")
                
        # Check for required fields
        if "legal_disclaimer" not in data and self.compliance_rules["require_disclaimers"]:
            issues.append("Missing required legal disclaimer")
            
        return len(issues) == 0, issues
        
    def anonymize_source(self, source_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Anonymize data source information.
        
        Args:
            source_info: Source information
            
        Returns:
            Anonymized source information
        """
        if not self.compliance_rules["anonymize_sources"]:
            return source_info
            
        anonymized = {
            "source_type": source_info.get("type", "unknown"),
            "confidence": source_info.get("confidence", 0.0),
            "timestamp": source_info.get("timestamp", ""),
        }
        
        # Remove identifying information
        return anonymized


if __name__ == "__main__":
    sanitizer = LegalSanitizer()
    test_text = "Contact john.doe@example.com or call 555-123-4567 for details."
    result = sanitizer.sanitize_text(test_text)
    print(f"Sanitized: {result}")
