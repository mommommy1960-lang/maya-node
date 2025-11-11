# SPDX-License-Identifier: CERL-1.0
# Copyright (c) 2025 MAYA Node Contributors
# 
# Constrained Ethics Runtime License 1.0
# This code is licensed under CERL-1.0. See LICENSE-CERL-1.0 for full terms.

"""
Role-Based Access Control (RBAC)

Implements role-based access control for secure permission management.
"""

import logging
from typing import Set, Dict, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Role:
    """Role definition"""
    name: str
    permissions: Set[str]
    description: str


class RBAC:
    """
    Role-Based Access Control system.
    
    Manages roles and permissions to control access to resources.
    """
    
    def __init__(self):
        """Initialize RBAC system."""
        self.roles: Dict[str, Role] = {}
        self.user_roles: Dict[str, Set[str]] = {}
        
        # Define default roles
        self._initialize_default_roles()
        
        logger.info("RBAC system initialized")
    
    def _initialize_default_roles(self) -> None:
        """Set up default roles."""
        
        # Admin role
        self.add_role(Role(
            name="admin",
            permissions={
                "read", "write", "delete", "manage_users",
                "manage_roles", "view_audit_log"
            },
            description="Full system access"
        ))
        
        # Operator role
        self.add_role(Role(
            name="operator",
            permissions={"read", "write", "view_audit_log"},
            description="Standard operations"
        ))
        
        # Viewer role
        self.add_role(Role(
            name="viewer",
            permissions={"read"},
            description="Read-only access"
        ))
    
    def add_role(self, role: Role) -> None:
        """
        Add a new role.
        
        Args:
            role: Role to add
        """
        self.roles[role.name] = role
        logger.info(f"Role added: {role.name}")
    
    def assign_role(self, user_id: str, role_name: str) -> bool:
        """
        Assign role to user.
        
        Args:
            user_id: User identifier
            role_name: Name of role to assign
            
        Returns:
            True if assigned successfully
        """
        if role_name not in self.roles:
            logger.error(f"Role not found: {role_name}")
            return False
        
        if user_id not in self.user_roles:
            self.user_roles[user_id] = set()
        
        self.user_roles[user_id].add(role_name)
        logger.info(f"Assigned role {role_name} to user {user_id}")
        return True
    
    def has_permission(self, user_id: str, permission: str) -> bool:
        """
        Check if user has permission.
        
        Args:
            user_id: User identifier
            permission: Permission to check
            
        Returns:
            True if user has permission
        """
        if user_id not in self.user_roles:
            return False
        
        for role_name in self.user_roles[user_id]:
            role = self.roles.get(role_name)
            if role and permission in role.permissions:
                return True
        
        return False
    
    def get_user_permissions(self, user_id: str) -> Set[str]:
        """
        Get all permissions for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Set of permissions
        """
        permissions = set()
        
        if user_id in self.user_roles:
            for role_name in self.user_roles[user_id]:
                role = self.roles.get(role_name)
                if role:
                    permissions.update(role.permissions)
        
        return permissions


if __name__ == "__main__":
    rbac = RBAC()
    
    # Assign roles
    rbac.assign_role("user1", "admin")
    rbac.assign_role("user2", "viewer")
    
    # Check permissions
    print(f"user1 can write: {rbac.has_permission('user1', 'write')}")
    print(f"user2 can write: {rbac.has_permission('user2', 'write')}")
    print(f"user1 permissions: {rbac.get_user_permissions('user1')}")
