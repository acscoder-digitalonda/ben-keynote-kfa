# Keynote KFA - Streamlit Version

A modern, interactive web application for AI-powered keynote analysis built with Streamlit.

## 🚀 Quick Start

### Option 1: Using the launcher script
```bash
python run_streamlit.py
```

### Option 2: Direct Streamlit command
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 📋 Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## 🎯 Features

### Modern UI/UX
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Interactive Interface**: Real-time feedback and progress indicators
- **Professional Styling**: Clean, modern design with custom CSS
- **Intuitive Navigation**: Easy-to-use sidebar and tabbed interface

### File Processing
- **Multiple Formats**: Support for `.txt`, `.md`, `.docx`, and `.srt` files
- **Drag & Drop Upload**: Simple file upload with size validation
- **Real-time Progress**: Visual progress indicators during processing
- **Error Handling**: Comprehensive error messages and recovery

### Analysis Features
- **Configurable Settings**: Adjust chunk size, overlap, temperature, and more
- **Two Processing Strategies**:
  - Token-based chunking (recommended for most use cases)
  - Scene map analysis (advanced, for structured content)
- **AI-Powered Critique**: Uses OpenAI models for intelligent analysis

### Results & Export
- **Multiple Download Formats**: Markdown and CSV exports
- **Interactive Preview**: Rendered markdown and raw source views
- **Data Visualization**: Analysis statistics and metrics
- **CSV Data Table**: Interactive table view of chunked analysis

### Advanced Features
- **Statistics Dashboard**: Document metrics and analysis insights
- **Configurable Parameters**: Fine-tune AI behavior through sidebar
- **Session Management**: Clean state management between analyses
- **Performance Optimized**: Efficient file handling and processing

## 🔧 Configuration

### Environment Variables
Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
KFA_GLOBAL_MODEL=gpt-4  # Optional: override default model
KFA_STYLE_MODEL=gpt-4o-mini  # Optional: override default model
```

### Config File
Copy `config.example.yaml` to `config.yaml` and customize:
```yaml
provider: openai

models:
  global_model: gpt-4
  style_model: gpt-4o-mini

params:
  temperature: 0.2
  max_output_tokens: 1500

chunking:
  strategy: tokens
  chunk_tokens: 2000
  overlap_tokens: 200
  prefer_sentence_boundary: true

io:
  input_format: auto
  export_md: true
  export_docx: false
  export_csv: true
```

## 📱 Interface Overview

### Main Upload Area
- **File Upload**: Drag and drop or click to select files
- **Format Support**: Visual indicators for supported file types
- **File Validation**: Real-time file size and format checking

### Sidebar Configuration
- **Processing Strategy**: Choose between token-based or scene map analysis
- **Advanced Settings**: Fine-tune chunking and AI parameters
- **Help Information**: Contextual help and format support details

### Results Display
- **Success Indicators**: Clear visual feedback when processing completes
- **Download Buttons**: One-click download for markdown and CSV files
- **Preview Tabs**: 
  - **Rendered**: Formatted markdown display
  - **Raw Markdown**: Source code view
  - **Statistics**: Document metrics and analysis insights
- **Data Table**: Interactive CSV data with sorting and filtering

## 🎨 Customization

### Themes
The app uses a custom theme defined in `.streamlit/config.toml`:
- Primary color: `#667eea` (blue gradient)
- Background: Clean white with subtle gray accents
- Typography: Modern sans-serif font stack

### Custom CSS
The app includes extensive custom CSS for:
- Gradient headers and badges
- Card-based layouts
- Responsive design
- Interactive elements
- Professional styling

## 🔍 Comparison: Streamlit vs FastAPI

| Feature | Streamlit Version | FastAPI Version |
|---------|------------------|-----------------|
| **Setup Complexity** | ⭐⭐⭐⭐⭐ Simple | ⭐⭐⭐ Moderate |
| **UI/UX** | ⭐⭐⭐⭐⭐ Modern & Interactive | ⭐⭐⭐ Basic HTML |
| **Responsiveness** | ⭐⭐⭐⭐⭐ Built-in | ⭐⭐⭐ Custom CSS |
| **Real-time Feedback** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐ Limited |
| **Data Visualization** | ⭐⭐⭐⭐⭐ Rich widgets | ⭐⭐ Basic tables |
| **Configuration** | ⭐⭐⭐⭐⭐ Interactive sidebar | ⭐⭐ Static form |
| **Error Handling** | ⭐⭐⭐⭐⭐ User-friendly | ⭐⭐⭐ Technical |
| **Mobile Support** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Good |

## 🚀 Deployment

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Production Deployment
For production deployment, consider:
- **Streamlit Cloud**: Easy deployment with GitHub integration
- **Docker**: Containerized deployment
- **Cloud Platforms**: AWS, GCP, Azure with Streamlit support

## 🛠️ Development

### Project Structure
```
keynote-kfa/
├── app.py                 # Main Streamlit application
├── run_streamlit.py       # Launcher script
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── kfa/                  # Core analysis modules (unchanged)
├── requirements.txt      # Updated dependencies
└── README_STREAMLIT.md   # This file
```

### Key Benefits of Streamlit Version
1. **Rapid Development**: Much faster to build and iterate
2. **Built-in Widgets**: Rich UI components out of the box
3. **Automatic Responsiveness**: Mobile-friendly by default
4. **State Management**: Simplified session state handling
5. **Data Integration**: Excellent pandas/dataframe support
6. **Deployment Options**: Multiple easy deployment paths

## 📝 Usage Tips

1. **File Size**: Keep files under 200MB for optimal performance
2. **Processing Time**: Larger files may take several minutes to process
3. **Configuration**: Use the sidebar to adjust settings before processing
4. **Results**: Download files immediately after processing
5. **New Analysis**: Use the "New Analysis" button to start over

## 🤝 Contributing

The Streamlit version maintains the same core functionality while providing a much better user experience. Contributions are welcome for:
- UI/UX improvements
- Additional visualization features
- Performance optimizations
- New export formats
- Enhanced error handling

## 📄 License

Same license as the main project.