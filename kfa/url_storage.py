"""
URL-based configuration storage using Streamlit query parameters
"""
import streamlit as st
import json
import base64
from typing import Dict, Any, Optional


def save_config_to_url(config_data: Dict[str, Any]) -> None:
    """Save configuration to URL parameters"""
    try:
        # Encode config data
        config_json = json.dumps(config_data)
        config_b64 = base64.b64encode(config_json.encode()).decode()
        
        # Update query parameters
        st.query_params.config = config_b64
        
        # Also save to session state
        st.session_state.user_config = config_data
        
    except Exception as e:
        # Fallback to session state only
        st.session_state.user_config = config_data


def load_config_from_url() -> Optional[Dict[str, Any]]:
    """Load configuration from URL parameters or session state"""
    
    # First check session state
    if 'user_config' in st.session_state:
        return st.session_state.user_config
    
    # Try to load from URL parameters
    try:
        if 'config' in st.query_params:
            config_b64 = st.query_params.config
            config_json = base64.b64decode(config_b64).decode()
            config_data = json.loads(config_json)
            
            # Store in session state for this session
            st.session_state.user_config = config_data
            return config_data
            
    except Exception:
        pass  # Ignore decoding errors
    
    return None


def clear_config_from_url() -> None:
    """Clear configuration from URL and session state"""
    
    # Clear session state
    if 'user_config' in st.session_state:
        del st.session_state.user_config
    
    # Clear URL parameter
    try:
        if 'config' in st.query_params:
            del st.query_params.config
    except Exception:
        pass