# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Tests for TPM Attestation Stub
"""

import unittest
from src.sovereign.tpm_attestation import (
    TPMAttestationStub,
    AttestationStatus,
    PlatformMeasurement
)


class TestTPMAttestation(unittest.TestCase):
    """Test cases for TPM attestation stub"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.attestation = TPMAttestationStub()
    
    def test_initialization(self):
        """Test TPM stub initialization"""
        self.assertIsNotNone(self.attestation)
        self.assertFalse(self.attestation.tpm_available)
    
    def test_tpm_availability_check(self):
        """Test TPM availability detection"""
        available = self.attestation.check_tpm_available()
        self.assertIsInstance(available, bool)
        # In stub mode, should be False
        self.assertFalse(available)
    
    def test_get_platform_measurements(self):
        """Test getting platform measurements"""
        measurements = self.attestation.get_platform_measurements()
        
        self.assertIsInstance(measurements, list)
        self.assertGreater(len(measurements), 0)
        
        # Verify measurement structure
        for m in measurements:
            self.assertIsInstance(m, PlatformMeasurement)
            self.assertIsInstance(m.pcr_index, int)
            self.assertIsInstance(m.measurement, str)
            self.assertIsInstance(m.component, str)
            self.assertGreater(m.timestamp, 0)
    
    def test_verify_platform_integrity_unavailable(self):
        """Test integrity verification in stub mode"""
        result = self.attestation.verify_platform_integrity()
        
        self.assertIsNotNone(result)
        # In stub mode without TPM, should be UNAVAILABLE
        self.assertEqual(result.status, AttestationStatus.UNAVAILABLE)
        self.assertFalse(result.tpm_available)
        self.assertGreater(len(result.measurements), 0)
    
    def test_attestation_report_generation(self):
        """Test attestation report generation"""
        report = self.attestation.generate_attestation_report()
        
        self.assertIsInstance(report, dict)
        self.assertIn("version", report)
        self.assertIn("timestamp", report)
        self.assertIn("tpm_available", report)
        self.assertIn("status", report)
        self.assertIn("measurements", report)
        
        self.assertEqual(report["status"], "stub_mode")
        self.assertFalse(report["tpm_available"])
    
    def test_pcr_extend_stub(self):
        """Test PCR extension stub"""
        result = self.attestation.extend_pcr(10, b"test_data")
        # In stub mode, should return True
        self.assertTrue(result)
    
    def test_measurement_pcr_indices(self):
        """Test that measurements use valid PCR indices"""
        measurements = self.attestation.get_platform_measurements()
        
        for m in measurements:
            # PCR indices should be 0-23 (standard TPM 2.0)
            self.assertGreaterEqual(m.pcr_index, 0)
            self.assertLessEqual(m.pcr_index, 23)
    
    def test_measurement_hash_format(self):
        """Test that measurements are valid hex strings"""
        measurements = self.attestation.get_platform_measurements()
        
        for m in measurements:
            # SHA256 hash should be 64 hex characters
            self.assertEqual(len(m.measurement), 64)
            # Should be valid hex
            try:
                int(m.measurement, 16)
            except ValueError:
                self.fail(f"Invalid hex hash: {m.measurement}")


class TestAttestationStatus(unittest.TestCase):
    """Test cases for attestation status enum"""
    
    def test_status_values(self):
        """Test attestation status enum values"""
        statuses = [
            AttestationStatus.VERIFIED,
            AttestationStatus.UNVERIFIED,
            AttestationStatus.FAILED,
            AttestationStatus.UNAVAILABLE
        ]
        
        for status in statuses:
            self.assertIsInstance(status, AttestationStatus)
            self.assertIsInstance(status.value, str)


class TestTPMWithExpectedMeasurements(unittest.TestCase):
    """Test TPM verification with expected measurements"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.attestation = TPMAttestationStub()
        # Simulate TPM being available for these tests
        self.attestation.tpm_available = True
    
    def test_verification_with_matching_measurements(self):
        """Test verification succeeds with matching measurements"""
        # Get actual measurements
        measurements = self.attestation.get_platform_measurements()
        
        # Build expected measurements dict
        expected = {
            m.pcr_index: m.measurement
            for m in measurements
        }
        
        # Should verify successfully
        result = self.attestation.verify_platform_integrity(expected)
        self.assertEqual(result.status, AttestationStatus.VERIFIED)
    
    def test_verification_with_mismatched_measurements(self):
        """Test verification fails with mismatched measurements"""
        # Provide wrong expected measurements
        expected = {
            0: "0" * 64,  # Wrong hash
            7: "f" * 64   # Wrong hash
        }
        
        result = self.attestation.verify_platform_integrity(expected)
        self.assertEqual(result.status, AttestationStatus.FAILED)
    
    def test_verification_without_expected(self):
        """Test verification without expected measurements"""
        result = self.attestation.verify_platform_integrity()
        # Should succeed when no expected measurements provided
        self.assertEqual(result.status, AttestationStatus.VERIFIED)


if __name__ == '__main__':
    unittest.main()
