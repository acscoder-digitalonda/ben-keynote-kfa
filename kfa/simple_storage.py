"""
Simple storage implementation using URL parameters and session state
"""
import streamlit as st
from typing import Dict, Any, Optional
from .url_storage import save_config_to_url, load_config_from_url, clear_config_from_url


def save_config_simple(config_data: Dict[str, Any]) -> None:
    """Save configuration using URL storage"""
    save_config_to_url(config_data)


def load_config_simple() -> Optional[Dict[str, Any]]:
    """Load configuration from URL storage"""
    return load_config_from_url()


def clear_config_simple() -> None:
    """Clear configuration from URL storage"""
    clear_config_from_url()


def get_config_value_simple(key: str, default: Any = None) -> Any:
    """Get specific config value"""
    config = load_config_simple()
    return config.get(key, default) if config else default


def update_config_value_simple(key: str, value: Any) -> None:
    """Update specific config value"""
    config = load_config_simple() or {}
    config[key] = value
    save_config_simple(config)