"""
Browser storage utilities for remembering configuration parameters
"""
import streamlit as st
import json
from typing import Dict, Any, Optional


def save_config_to_browser(config_key: str, config_data: Dict[str, Any]) -> None:
    """Save configuration to browser localStorage"""
    config_json = json.dumps(config_data)
    
    # JavaScript to save to localStorage
    js_code = f"""
    <script>
        localStorage.setItem('{config_key}', '{config_json}');
    </script>
    """
    st.components.v1.html(js_code, height=0)


def load_config_from_browser(config_key: str) -> Optional[Dict[str, Any]]:
    """Load configuration from browser localStorage"""
    
    # JavaScript to retrieve from localStorage
    js_code = f"""
    <script>
        const config = localStorage.getItem('{config_key}');
        if (config) {{
            parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: config
            }}, '*');
        }}
    </script>
    """
    
    # Use session state to store the retrieved value
    if f"{config_key}_loaded" not in st.session_state:
        st.session_state[f"{config_key}_loaded"] = None
        
    # Display the JavaScript component
    result = st.components.v1.html(js_code, height=0)
    
    if result:
        try:
            return json.loads(result)
        except (json.JSONDecodeError, TypeError):
            return None
    
    return st.session_state.get(f"{config_key}_loaded")


def get_default_config() -> Dict[str, Any]:
    """Get default configuration values"""
    return {
        'strategy': 'tokens',
        'chunk_tokens': 2000,
        'overlap_tokens': 200,
        'temperature': 0.2,
        'max_output_tokens': 1500
    }


def merge_with_defaults(saved_config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Merge saved config with defaults"""
    defaults = get_default_config()
    
    if saved_config:
        defaults.update(saved_config)
    
    return defaults