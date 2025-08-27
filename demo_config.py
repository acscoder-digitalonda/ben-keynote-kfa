#!/usr/bin/env python3
"""
Demo script to test configuration remembering functionality
"""
import streamlit as st
from kfa.config_manager import ConfigManager

# Configure page
st.set_page_config(
    page_title="Config Demo",
    page_icon="⚙️",
    layout="wide"
)

def main():
    st.title("⚙️ Configuration Memory Demo")
    st.markdown("This demo shows how configuration parameters are remembered across sessions.")
    
    # Initialize config manager with cookies (100 days)
    config_manager = ConfigManager(storage_type="cookie")
    st.info("🍪 Using browser cookies - settings persist for 100 days")
    
    st.markdown("---")
    
    # Configuration section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎛️ Settings")
        
        # Get current config
        current_config = config_manager.get_merged_config()
        
        # Configuration inputs
        strategy = st.selectbox(
            "Processing Strategy",
            options=["tokens", "scene_map"],
            index=0 if current_config.get("strategy") == "tokens" else 1
        )
        
        chunk_tokens = st.slider(
            "Chunk Size", 
            500, 4000, 
            current_config.get("chunk_tokens", 2000)
        )
        
        temperature = st.slider(
            "Temperature", 
            0.0, 1.0, 
            current_config.get("temperature", 0.2),
            0.1
        )
        
        # Create new config
        new_config = {
            'strategy': strategy,
            'chunk_tokens': chunk_tokens,
            'temperature': temperature
        }
        
        # Auto-save configuration on any change
        config_manager.save_config(new_config)
        
        # Show auto-save status
        st.success("✅ Settings auto-saved!")
    
    with col2:
        st.subheader("📊 Current Configuration")
        
        # Show current config
        loaded_config = config_manager.load_config()
        
        if loaded_config:
            st.json(loaded_config)
            st.success("✅ Configuration loaded from cookies")
        else:
            st.info("No saved configuration found")
        
        st.subheader("🔧 Merged with Defaults")
        st.json(config_manager.get_merged_config())
        
        # Instructions
        st.markdown("---")
        st.markdown("### 📝 Instructions")
        st.markdown("""
        1. **Adjust settings** on the left
        2. **Settings auto-save** to browser cookies
        3. **Refresh page** to test persistence
        4. **Close and reopen browser** - settings will persist for 100 days
        5. **Check browser dev tools Console** for cookie logs
        """)
        
        st.success("🍪 Cookies persist for 100 days until manually cleared")

if __name__ == "__main__":
    main()