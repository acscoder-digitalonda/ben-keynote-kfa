#!/usr/bin/env python3
"""
Demo for reliable configuration storage
"""
import streamlit as st
from kfa.config_manager import ConfigManager, create_config_sidebar

# Configure page
st.set_page_config(
    page_title="Reliable Config Demo",
    page_icon="💾",
    layout="wide"
)

def main():
    st.title("💾 Reliable Configuration Demo")
    st.markdown("This demo shows configuration persistence using session state + URL parameters.")
    
    # Initialize config manager with reliable storage
    config_manager = ConfigManager(storage_type="reliable")
    
    st.info("💾 Using session state + URL parameters - settings persist during session and can be bookmarked")
    
    st.markdown("---")
    
    # Configuration section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        user_config = create_config_sidebar(config_manager)
    
    with col2:
        st.subheader("📊 Current Configuration")
        
        # Show current config
        loaded_config = config_manager.load_config()
        
        if loaded_config:
            st.json(loaded_config)
            st.success("✅ Configuration loaded successfully")
        else:
            st.info("No saved configuration found")
        
        st.subheader("🔧 Merged with Defaults")
        st.json(config_manager.get_merged_config())
        
        # Manual controls
        col_clear, col_info = st.columns(2)
        with col_clear:
            if st.button("🗑️ Clear Config"):
                config_manager.clear_config()
                st.success("Configuration cleared!")
                st.rerun()
        
        with col_info:
            if st.button("🔄 Refresh Page"):
                st.rerun()
        
        # Instructions
        st.markdown("---")
        st.markdown("### 📝 Instructions")
        st.markdown("""
        1. **Adjust settings** on the left
        2. **Settings auto-save** to session state
        3. **Click "Refresh Page"** to test persistence
        4. **Bookmark the URL** to save your configuration
        5. **Settings persist during browser session**
        """)
        
        # Show current URL for bookmarking
        if 'config' in st.query_params:
            st.success("🔗 Current URL contains your configuration - bookmark it!")
        else:
            st.info("🔗 Adjust settings to generate a bookmarkable URL")

if __name__ == "__main__":
    main()