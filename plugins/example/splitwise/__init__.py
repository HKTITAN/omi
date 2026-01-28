"""
Splitwise Integration Plugin for Omi

This plugin provides Splitwise expense management integration
with Omi's chat tools system.

See main.py for chat tools implementation.
See oauth.py for OAuth authentication flow.
"""

from .main import router as main_router
from .oauth import router as oauth_router

__all__ = ['main_router', 'oauth_router']
