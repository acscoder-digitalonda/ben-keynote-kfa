"""
Simple browser-based configuration storage using cookies
"""
import streamlit as st
import streamlit.components.v1 as components
import json
from typing import Dict, Any, Optional


def save_config_to_browser(config_data: Dict[str, Any]) -> None:
    """Save configuration to browser cookies"""
    
    # Also save to session state as backup
    st.session_state.user_config = config_data
    
    # Create JavaScript to save to cookies
    config_json = json.dumps(config_data)
    
    js_code = f"""
    <script>
        function setCookie(name, value, days) {{
            const expires = new Date();
            expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
            document.cookie = name + '=' + encodeURIComponent(value) + ';expires=' + expires.toUTCString() + ';path=/';
        }}
        
        setCookie('keynote_kfa_config', '{config_json}', 30);
    </script>
    """
    
    components.html(js_code, height=0)


def load_config_from_browser() -> Optional[Dict[str, Any]]:
    """Load configuration from browser cookies or session state"""
    
    # First check session state
    if 'user_config' in st.session_state:
        return st.session_state.user_config
    
    # Try to load from cookies using JavaScript
    js_code = """
    <script>
        function getCookie(name) {
            const nameEQ = name + "=";
            const ca = document.cookie.split(';');
            for(let i = 0; i < ca.length; i++) {
                let c = ca[i];
                while (c.charAt(0) === ' ') c = c.substring(1, c.length);
                if (c.indexOf(nameEQ) === 0) {
                    return decodeURIComponent(c.substring(nameEQ.length, c.length));
                }
            }
            return null;
        }
        
        const configCookie = getCookie('keynote_kfa_config');
        if (configCookie) {
            try {
                const config = JSON.parse(configCookie);
                // Send to Streamlit
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: config
                }, '*');
            } catch (e) {
                console.error('Failed to parse config cookie:', e);
            }
        }
    </script>
    """
    
    result = components.html(js_code, height=0)
    
    if result and isinstance(result, dict):
        # Store in session state for this session
        st.session_state.user_config = result
        return result
    
    return None


def clear_config_from_browser() -> None:
    """Clear configuration from browser and session"""
    
    # Clear session state
    if 'user_config' in st.session_state:
        del st.session_state.user_config
    
    # Clear cookie
    js_code = """
    <script>
        document.cookie = 'keynote_kfa_config=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    </script>
    """
    
    components.html(js_code, height=0)