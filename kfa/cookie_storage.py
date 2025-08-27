"""
Cookie-based storage for configuration parameters
"""
import streamlit as st
import streamlit.components.v1 as components
import json
import base64
from typing import Dict, Any, Optional


def save_config_cookie(config_data: Dict[str, Any], days: int = 100) -> None:
    """Save configuration to browser cookies"""
    
    # Also save to session state as backup
    st.session_state.user_config = config_data
    
    # Encode config data
    config_json = json.dumps(config_data)
    config_b64 = base64.b64encode(config_json.encode()).decode()
    
    # JavaScript to set cookie
    js_code = f"""
    <script>
        function setCookie(name, value, days) {{
            const expires = new Date();
            expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
            document.cookie = name + '=' + encodeURIComponent(value) + ';expires=' + expires.toUTCString() + ';path=/';
            console.log('Config saved to cookie for ' + days + ' days');
        }}
        
        setCookie('keynote_kfa_config', '{config_b64}', {days});
    </script>
    """
    
    components.html(js_code, height=0)


def load_config_cookie() -> Optional[Dict[str, Any]]:
    """Load configuration from browser cookies"""
    
    # First check session state
    if 'user_config' in st.session_state:
        return st.session_state.user_config
    
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
                const configJson = atob(configCookie);
                const config = JSON.parse(configJson);
                console.log('Config loaded from cookie:', config);
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: config
                }, '*');
            } catch (e) {
                console.error('Failed to parse config cookie:', e);
            }
        } else {
            console.log('No config cookie found');
        }
    </script>
    """
    
    result = components.html(js_code, height=0)
    
    if result and isinstance(result, dict):
        # Store in session state for this session
        st.session_state.user_config = result
        return result
    
    return None


def clear_config_cookie() -> None:
    """Clear configuration cookie"""
    
    # Clear session state
    if 'user_config' in st.session_state:
        del st.session_state.user_config
    
    js_code = """
    <script>
        document.cookie = 'keynote_kfa_config=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        console.log('Config cookie cleared');
    </script>
    """
    
    components.html(js_code, height=0)


def get_cookie_value(key: str, default: Any = None) -> Any:
    """Get specific value from cookie config"""
    config = load_config_cookie()
    return config.get(key, default) if config else default