"""
Persistent browser storage component for configuration parameters
"""
import streamlit as st
import streamlit.components.v1 as components
import json
from typing import Dict, Any, Optional


def create_storage_component():
    """Create HTML/JS component for localStorage operations"""
    
    html_code = """
    <div id="storage-component" style="display: none;"></div>
    <script>
        // Storage operations
        window.saveToStorage = function(key, data) {
            try {
                localStorage.setItem(key, JSON.stringify(data));
                return true;
            } catch (e) {
                console.error('Failed to save to localStorage:', e);
                return false;
            }
        };
        
        window.loadFromStorage = function(key) {
            try {
                const data = localStorage.getItem(key);
                return data ? JSON.parse(data) : null;
            } catch (e) {
                console.error('Failed to load from localStorage:', e);
                return null;
            }
        };
        
        window.clearStorage = function(key) {
            try {
                localStorage.removeItem(key);
                return true;
            } catch (e) {
                console.error('Failed to clear localStorage:', e);
                return false;
            }
        };
        
        // Auto-load configuration on page load
        window.addEventListener('load', function() {
            const config = window.loadFromStorage('keynote_kfa_config');
            if (config) {
                // Send config to Streamlit
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: config
                }, '*');
            }
        });
        
        // Listen for save requests from Streamlit
        window.addEventListener('message', function(event) {
            if (event.data.type === 'save_config') {
                window.saveToStorage('keynote_kfa_config', event.data.config);
            } else if (event.data.type === 'clear_config') {
                window.clearStorage('keynote_kfa_config');
            }
        });
    </script>
    """
    
    return components.html(html_code, height=0)


def save_config_persistent(config_data: Dict[str, Any]) -> None:
    """Save configuration to persistent browser storage"""
    
    # Store in session state as backup
    st.session_state.persistent_config = config_data
    
    # JavaScript to save to localStorage
    js_save = f"""
    <script>
        if (window.saveToStorage) {{
            window.saveToStorage('keynote_kfa_config', {json.dumps(config_data)});
        }}
    </script>
    """
    
    components.html(js_save, height=0)


def load_config_persistent() -> Optional[Dict[str, Any]]:
    """Load configuration from persistent browser storage"""
    
    # Try to get from session state first
    if 'persistent_config' in st.session_state:
        return st.session_state.persistent_config
    
    # JavaScript to load from localStorage
    js_load = """
    <script>
        if (window.loadFromStorage) {
            const config = window.loadFromStorage('keynote_kfa_config');
            if (config) {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: config
                }, '*');
            }
        }
    </script>
    """
    
    result = components.html(js_load, height=0)
    
    if result:
        st.session_state.persistent_config = result
        return result
    
    return None


def clear_config_persistent() -> None:
    """Clear persistent configuration"""
    
    # Clear from session state
    if 'persistent_config' in st.session_state:
        del st.session_state.persistent_config
    
    # JavaScript to clear localStorage
    js_clear = """
    <script>
        if (window.clearStorage) {
            window.clearStorage('keynote_kfa_config');
        }
    </script>
    """
    
    components.html(js_clear, height=0)


def get_persistent_value(key: str, default: Any = None) -> Any:
    """Get specific value from persistent config"""
    config = load_config_persistent()
    return config.get(key, default) if config else default