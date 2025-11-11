# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Content-Addressed Storage

Implements content-addressed storage with integrity verification.
"""

import logging
import hashlib
from typing import Optional, Dict

logger = logging.getLogger(__name__)


class ContentAddressedStorage:
    """
    Content-addressed storage system.
    
    Data is addressed by its cryptographic hash, ensuring:
    - Immutability
    - Deduplication
    - Integrity verification
    """
    
    def __init__(self):
        """Initialize CAS."""
        self.store: Dict[str, bytes] = {}
        logger.info("Content-Addressed Storage initialized")
    
    def put(self, data: bytes) -> str:
        """
        Store data and return its address.
        
        Args:
            data: Data to store
            
        Returns:
            Content address (hash)
        """
        address = hashlib.sha256(data).hexdigest()
        self.store[address] = data
        logger.info(f"Stored content at {address[:16]}...")
        return address
    
    def get(self, address: str) -> Optional[bytes]:
        """
        Retrieve data by address.
        
        Args:
            address: Content address
            
        Returns:
            Data if found, None otherwise
        """
        return self.store.get(address)
    
    def verify(self, address: str, data: bytes) -> bool:
        """
        Verify data matches its address.
        
        Args:
            address: Claimed address
            data: Data to verify
            
        Returns:
            True if data matches address
        """
        actual_address = hashlib.sha256(data).hexdigest()
        return actual_address == address


if __name__ == "__main__":
    cas = ContentAddressedStorage()
    test_data = b"Hello, MAYA Node!"
    addr = cas.put(test_data)
    print(f"Stored at: {addr}")
    retrieved = cas.get(addr)
    print(f"Verified: {cas.verify(addr, retrieved)}")
