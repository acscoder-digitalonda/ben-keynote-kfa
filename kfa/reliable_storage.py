"""
Reliable storage using session state with URL parameter backup
"""
import streamlit as st
import json
import base64
from typing import Dict, Any, Optional


def save_config_reliable(config_data: Dict[str, Any]) -> None:
    """Save configuration reliably using session state and URL"""
    
    # Always save to session state
    st.session_state.user_config = config_data
    
    # Try to save to URL parameters for sharing/bookmarking
    try:
        config_json = json.dumps(config_data, sort_keys=True)
        config_b64 = base64.b64encode(config_json.encode()).decode()
        
        # Update URL parameters
        st.query_params.config = config_b64
        
    except Exception:
        # If URL fails, that's okay - session state is primary
        pass


def load_config_reliable() -> Optional[Dict[str, Any]]:
    """Load configuration from session state or URL parameters"""
    
    # First priority: session state (works during session)
    if 'user_config' in st.session_state:
        return st.session_state.user_config
    
    # Second priority: URL parameters (for bookmarks/sharing)
    try:
        if 'config' in st.query_params:
            config_b64 = st.query_params.config
            config_json = base64.b64decode(config_b64).decode()
            config_data = json.loads(config_json)
            
            # Store in session state for this session
            st.session_state.user_config = config_data
            return config_data
            
    except Exception:
        pass  # Ignore URL parameter errors
    
    return None


def clear_config_reliable() -> None:
    """Clear configuration from session state and URL"""
    
    # Clear session state
    if 'user_config' in st.session_state:
        del st.session_state.user_config
    
    # Clear URL parameter
    try:
        if 'config' in st.query_params:
            del st.query_params.config
    except Exception:
        pass


def get_reliable_value(key: str, default: Any = None) -> Any:
    """Get specific config value"""
    config = load_config_reliable()
    return config.get(key, default) if config else default