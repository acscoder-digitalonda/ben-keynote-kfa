"""
Unified configuration manager for remembering user settings
"""
import streamlit as st
from typing import Dict, Any, Optional, Literal
from .session_storage import (
    save_config_to_session,
    load_config_from_session,
    get_config_value as get_session_value,
    clear_config as clear_session_config
)
from .simple_storage import (
    save_config_simple,
    load_config_simple,
    clear_config_simple
)
from .reliable_storage import (
    save_config_reliable,
    load_config_reliable,
    clear_config_reliable
)

StorageType = Literal["session", "cookie", "localStorage", "reliable"]


class ConfigManager:
    """Manages configuration storage across different methods"""
    
    def __init__(self, storage_type: StorageType = "session"):
        self.storage_type = storage_type
        self.default_config = {
            'strategy': 'tokens',
            'chunk_tokens': 2000,
            'overlap_tokens': 200,
            'temperature': 0.2,
            'max_output_tokens': 1500
        }
    
    def save_config(self, config_data: Dict[str, Any]) -> None:
        """Save configuration using selected storage method"""
        if self.storage_type == "session":
            save_config_to_session(config_data)
        elif self.storage_type == "cookie":
            from .cookie_storage import save_config_cookie
            save_config_cookie(config_data)
        elif self.storage_type == "localStorage":
            # Use simple storage implementation
            save_config_simple(config_data)
        elif self.storage_type == "reliable":
            # Use reliable storage implementation
            save_config_reliable(config_data)
    
    def load_config(self) -> Optional[Dict[str, Any]]:
        """Load configuration using selected storage method"""
        if self.storage_type == "session":
            return load_config_from_session()
        elif self.storage_type == "cookie":
            from .cookie_storage import load_config_cookie
            return load_config_cookie()
        elif self.storage_type == "localStorage":
            # Use simple storage implementation
            return load_config_simple()
        elif self.storage_type == "reliable":
            # Use reliable storage implementation
            return load_config_reliable()
        return None
    
    def get_value(self, key: str, default: Any = None) -> Any:
        """Get specific configuration value"""
        config = self.load_config()
        if config and key in config:
            return config[key]
        return self.default_config.get(key, default)
    
    def update_value(self, key: str, value: Any) -> None:
        """Update specific configuration value"""
        config = self.load_config() or {}
        config[key] = value
        self.save_config(config)
    
    def clear_config(self) -> None:
        """Clear all configuration"""
        if self.storage_type == "session":
            clear_session_config()
        elif self.storage_type == "cookie":
            from .cookie_storage import clear_config_cookie
            clear_config_cookie()
        elif self.storage_type == "localStorage":
            # Use simple storage implementation
            clear_config_simple()
        elif self.storage_type == "reliable":
            # Use reliable storage implementation
            clear_config_reliable()
    
    def get_merged_config(self) -> Dict[str, Any]:
        """Get configuration merged with defaults"""
        saved_config = self.load_config() or {}
        merged = self.default_config.copy()
        merged.update(saved_config)
        return merged


def create_config_sidebar(config_manager: ConfigManager) -> Dict[str, Any]:
    """Create configuration sidebar with remembered settings"""
    
    st.header("⚙️ Configuration")
    
    # Load saved configuration once at the start
    saved_config = config_manager.load_config() or {}
    defaults = config_manager.default_config
    
    # Merge saved config with defaults
    current_values = defaults.copy()
    current_values.update(saved_config)
    
    # Processing strategy
    strategy = st.selectbox(
        "Processing Strategy",
        options=["tokens", "scene_map"],
        index=0 if current_values.get("strategy") == "tokens" else 1,
        format_func=lambda x: {
            "tokens": "Token-based Chunking (Recommended)",
            "scene_map": "Scene Map Analysis (Advanced)"
        }[x],
        help="Choose how to split your content for analysis"
    )
    
    # Advanced settings
    with st.expander("Advanced Settings"):
        chunk_tokens = st.slider(
            "Chunk Size (tokens)", 
            500, 4000, 
            current_values.get("chunk_tokens", 2000)
        )
        overlap_tokens = st.slider(
            "Overlap (tokens)", 
            50, 500, 
            current_values.get("overlap_tokens", 200)
        )
        temperature = st.slider(
            "AI Temperature", 
            0.0, 1.0, 
            current_values.get("temperature", 0.2), 
            0.1
        )
        max_output_tokens = st.slider(
            "Max Output Tokens", 
            500, 3000, 
            current_values.get("max_output_tokens", 1500)
        )
    
    # Create new configuration
    new_config = {
        'strategy': strategy,
        'chunk_tokens': chunk_tokens,
        'overlap_tokens': overlap_tokens,
        'temperature': temperature,
        'max_output_tokens': max_output_tokens
    }
    
    # Auto-save configuration on any change
    config_manager.save_config(new_config)
    
    return new_config