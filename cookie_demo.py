#!/usr/bin/env python3
"""
Demo for cookie-based configuration storage
"""
import streamlit as st
from kfa.config_manager import ConfigManager, create_config_sidebar

# Configure page
st.set_page_config(
    page_title="Cookie Config Demo",
    page_icon="🍪",
    layout="wide"
)

def main():
    st.title("🍪 Cookie Configuration Demo")
    st.markdown("This demo shows how configuration parameters are saved to browser cookies for 100 days.")
    
    # Initialize config manager with cookies
    config_manager = ConfigManager(storage_type="cookie")
    
    st.info("💾 Using browser cookies - settings persist for 100 days across browser sessions")
    
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
            st.success("✅ Configuration loaded from cookies")
        else:
            st.info("No saved configuration found")
        
        st.subheader("🔧 Merged with Defaults")
        st.json(config_manager.get_merged_config())
        
        # Manual controls
        col_clear, col_info = st.columns(2)
        with col_clear:
            if st.button("🗑️ Clear Cookies"):
                config_manager.clear_config()
                st.success("Cookies cleared!")
                st.rerun()
        
        with col_info:
            if st.button("ℹ️ Show Debug"):
                st.write("Session state keys:", list(st.session_state.keys()))
        
        # Instructions
        st.markdown("---")
        st.markdown("### 📝 Instructions")
        st.markdown("""
        1. **Adjust settings** on the left
        2. **Settings auto-save** to browser cookies
        3. **Refresh page** to test persistence
        4. **Close and reopen browser** - settings will persist for 100 days
        5. **Open browser dev tools** (F12) and check Console for cookie logs
        """)
        
        st.success("🍪 Cookies persist for 100 days until manually cleared")

if __name__ == "__main__":
    main()