"""
Session-based storage for configuration parameters using Streamlit session state
"""
import streamlit as st
from typing import Dict, Any, Optional


def save_config_to_session(config_data: Dict[str, Any]) -> None:
    """Save configuration to Streamlit session state"""
    st.session_state.user_config = config_data


def load_config_from_session() -> Optional[Dict[str, Any]]:
    """Load configuration from Streamlit session state"""
    return st.session_state.get('user_config')


def get_config_value(key: str, default: Any = None) -> Any:
    """Get specific config value from session"""
    config = load_config_from_session()
    return config.get(key, default) if config else default


def update_config_value(key: str, value: Any) -> None:
    """Update specific config value in session"""
    config = load_config_from_session() or {}
    config[key] = value
    save_config_to_session(config)


def clear_config() -> None:
    """Clear all saved configuration"""
    if 'user_config' in st.session_state:
        del st.session_state.user_config