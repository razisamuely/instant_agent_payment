"""
Paddle Payment Integration

A Python library for integrating with Paddle's payment API.
Supports both sandbox and production environments for managing
subscriptions and one-time purchases.
"""

__version__ = "0.1.0"
__author__ = "Instant Agent Payment"

from .paddle_client import PaddleClient

__all__ = ["PaddleClient"]
