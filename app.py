import streamlit as st
import tempfile
import os
import pathlib
import time
import pandas as pd
from typing import Optional
from kfa.cli import run as run_cli
from kfa.config import load_config

# Configure Streamlit page
st.set_page_config(
    page_title="Keynote KFA - AI-Powered Keynote Analysis",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
        margin: 1rem 0;
    }
    
    .results-section {
        background: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .success-badge {
        background: #28a745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .info-box {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 5px 5px 0;
    }
    
    .download-button {
        background: #007bff;
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 5px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem 0.5rem 0.5rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Keynote KFA</h1>
        <p>AI-powered keynote analysis tool that chunks, critiques, and generates clean outputs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Processing strategy
        strategy = st.selectbox(
            "Processing Strategy",
            options=["tokens", "scene_map"],
            format_func=lambda x: {
                "tokens": "Token-based Chunking (Recommended)",
                "scene_map": "Scene Map Analysis (Advanced)"
            }[x],
            help="Choose how to split your content for analysis"
        )
        
        # Advanced settings
        with st.expander("Advanced Settings"):
            chunk_tokens = st.slider("Chunk Size (tokens)", 500, 4000, 2000)
            overlap_tokens = st.slider("Overlap (tokens)", 50, 500, 200)
            temperature = st.slider("AI Temperature", 0.0, 1.0, 0.2, 0.1)
            max_output_tokens = st.slider("Max Output Tokens", 500, 3000, 1500)
        
        st.markdown("---")
        st.markdown("### 📋 Supported Formats")
        st.markdown("- `.txt` - Plain text files")
        st.markdown("- `.md` - Markdown files") 
        st.markdown("- `.docx` - Word documents")
        st.markdown("- `.srt` - Subtitle files")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.subheader("📁 Upload Your File")
        
        uploaded_file = st.file_uploader(
            "Choose a file to analyze",
            type=['txt', 'md', 'docx', 'srt'],
            help="Upload your keynote transcript, presentation notes, or any text document"
        )
        
        if uploaded_file is not None:
            # Display file info
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"📊 File size: {uploaded_file.size / 1024:.1f} KB")
            
            # Process button
            if st.button("🚀 Analyze Keynote", type="primary", use_container_width=True):
                process_file(uploaded_file, strategy, chunk_tokens, overlap_tokens, temperature, max_output_tokens)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### 🔍 How it works")
        st.markdown("""
        1. **Upload** your keynote file in any supported format
        2. **Choose** your processing strategy (tokens or scene map)
        3. **Analyze** - AI will chunk and critique your content
        4. **Download** the processed markdown and CSV outputs
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show example if no file uploaded
        if uploaded_file is None:
            st.markdown("### 📝 Example Content")
            with st.expander("View sample keynote text"):
                sample_path = pathlib.Path("data/examples/keynote_sample.txt")
                if sample_path.exists():
                    sample_text = sample_path.read_text()[:500] + "..."
                    st.text(sample_text)
                else:
                    st.info("No sample file found")

def process_file(uploaded_file, strategy, chunk_tokens, overlap_tokens, temperature, max_output_tokens):
    """Process the uploaded file and display results"""
    
    # Create progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Save uploaded file temporarily
        status_text.text("📁 Saving file...")
        progress_bar.progress(10)
        
        suffix = os.path.splitext(uploaded_file.name)[-1] or '.txt'
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        # Load and configure settings
        status_text.text("⚙️ Loading configuration...")
        progress_bar.progress(20)
        
        cfg = load_config('config.yaml')
        cfg['chunking']['strategy'] = strategy
        cfg['chunking']['chunk_tokens'] = chunk_tokens
        cfg['chunking']['overlap_tokens'] = overlap_tokens
        cfg['params']['temperature'] = temperature
        cfg['params']['max_output_tokens'] = max_output_tokens
        
        # Process the file
        status_text.text("🤖 Processing with AI...")
        progress_bar.progress(30)
        
        # Create output directory
        out_dir = pathlib.Path('out')
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # Run the analysis
        run_cli(tmp_path, cfg)
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        # Display results
        display_results()
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        progress_bar.empty()
        status_text.empty()

def display_results():
    """Display the analysis results"""
    
    st.markdown('<div class="results-section">', unsafe_allow_html=True)
    
    # Success message
    st.markdown('<div class="success-badge">🎉 Analysis Complete!</div>', unsafe_allow_html=True)
    
    # File paths
    md_path = pathlib.Path('out/keynote_kfa.md')
    csv_path = pathlib.Path('out/keynote_kfa_notes.csv')
    
    # Download buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if md_path.exists():
            with open(md_path, 'rb') as f:
                st.download_button(
                    label="📄 Download Markdown",
                    data=f.read(),
                    file_name="keynote_kfa.md",
                    mime="text/markdown",
                    use_container_width=True
                )
    
    with col2:
        if csv_path.exists():
            with open(csv_path, 'rb') as f:
                st.download_button(
                    label="📊 Download CSV Notes",
                    data=f.read(),
                    file_name="keynote_kfa_notes.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    with col3:
        # New analysis button
        if st.button("🔄 New Analysis", use_container_width=True):
            st.rerun()
    
    # Display CSV data if available
    if csv_path.exists():
        st.markdown("### 📊 Analysis Summary")
        try:
            df = pd.read_csv(csv_path)
            st.dataframe(df, use_container_width=True)
            
            # Show some basic stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Chunks", len(df))
            with col2:
                if 'text' in df.columns:
                    avg_length = df['text'].str.len().mean()
                    st.metric("Avg Chunk Length", f"{avg_length:.0f} chars")
            with col3:
                if 'kfa' in df.columns:
                    avg_kfa_length = df['kfa'].str.len().mean()
                    st.metric("Avg Analysis Length", f"{avg_kfa_length:.0f} chars")
                    
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    
    # Preview tabs
    if md_path.exists():
        st.markdown("### 👀 Content Preview")
        
        tab1, tab2, tab3 = st.tabs(["📖 Rendered", "📝 Raw Markdown", "📈 Statistics"])
        
        with tab1:
            # Read and display markdown content
            md_content = md_path.read_text(encoding='utf-8', errors='ignore')
            st.markdown(md_content[:15000])  # Increased preview size
            
            if len(md_content) > 15000:
                st.info("📄 Preview truncated. Download the full file to see all content.")
        
        with tab2:
            # Display raw markdown
            md_content = md_path.read_text(encoding='utf-8', errors='ignore')
            st.code(md_content[:8000], language='markdown')
            
            if len(md_content) > 8000:
                st.info("📄 Preview truncated. Download the full file to see all content.")
        
        with tab3:
            # Show document statistics
            md_content = md_path.read_text(encoding='utf-8', errors='ignore')
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Characters", len(md_content))
                st.metric("Total Words", len(md_content.split()))
                st.metric("Total Lines", len(md_content.split('\n')))
            
            with col2:
                # Count markdown elements
                headers = md_content.count('#')
                bold_text = md_content.count('**') // 2
                italic_text = md_content.count('*') - (bold_text * 2)
                
                st.metric("Headers", headers)
                st.metric("Bold Text", bold_text)
                st.metric("Italic Text", italic_text)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()