from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
from .cli import run as run_cli
from .config import load_config
import tempfile, os, pathlib, urllib.parse

app = FastAPI()

OUT_DIR = pathlib.Path('out')
OUT_DIR.mkdir(parents=True, exist_ok=True)

@app.get('/', response_class=HTMLResponse)
def index():
    return """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Keynote KFA — AI-Powered Keynote Analysis</title>
<style>
:root {
  --primary: #2563eb;
  --primary-dark: #1d4ed8;
  --secondary: #64748b;
  --success: #059669;
  --background: #f8fafc;
  --surface: #ffffff;
  --border: #e2e8f0;
  --text: #1e293b;
  --text-muted: #64748b;
  --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --radius: 0.75rem;
}

* {
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: var(--text);
  background: var(--background);
  margin: 0;
  padding: 0;
  min-height: 100vh;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

header {
  text-align: center;
  margin-bottom: 3rem;
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.logo-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.5rem;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 1.125rem;
  color: var(--text-muted);
  margin: 0.5rem 0 0 0;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 2rem;
  box-shadow: var(--shadow);
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: var(--shadow-lg);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text);
}

.file-input-wrapper {
  position: relative;
  display: inline-block;
  width: 100%;
}

input[type="file"] {
  width: 100%;
  padding: 0.75rem;
  border: 2px dashed var(--border);
  border-radius: var(--radius);
  background: var(--background);
  font-size: 1rem;
  transition: all 0.2s ease;
  cursor: pointer;
}

input[type="file"]:hover {
  border-color: var(--primary);
  background: var(--surface);
}

input[type="file"]:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgb(37 99 235 / 0.1);
}

select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  font-size: 1rem;
  transition: all 0.2s ease;
}

select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgb(37 99 235 / 0.1);
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  min-width: 140px;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}

.btn-primary:active {
  transform: translateY(0);
}

.supported-formats {
  margin-top: 1rem;
  padding: 1rem;
  background: var(--background);
  border-radius: var(--radius);
  border-left: 4px solid var(--primary);
}

.supported-formats h4 {
  margin: 0 0 0.5rem 0;
  color: var(--text);
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.format-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 0;
}

.format-tag {
  background: var(--surface);
  color: var(--text-muted);
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 500;
  border: 1px solid var(--border);
}

.loading {
  display: none;
  text-align: center;
  margin-top: 1rem;
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid var(--border);
  border-radius: 50%;
  border-top-color: var(--primary);
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 640px) {
  .container {
    padding: 1rem;
  }
  
  h1 {
    font-size: 2rem;
  }
  
  .card {
    padding: 1.5rem;
  }
  
  .format-list {
    justify-content: center;
  }
}
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="logo">
      <div class="logo-icon">K</div>
      <h1>Keynote KFA</h1>
    </div>
    <p class="subtitle">AI-powered keynote analysis tool that chunks, critiques, and generates clean outputs from your presentations and transcripts.</p>
  </header>
  
  <div class="card">
    <form action="/analyze" method="post" enctype="multipart/form-data" id="uploadForm">
      <div class="form-group">
        <label for="file">Select Your File</label>
        <input id="file" name="file" type="file" accept=".txt,.md,.docx,.srt" required />
      </div>
      
      <div class="form-group">
        <label for="strategy">Processing Strategy</label>
        <select id="strategy" name="strategy">
          <option value="tokens" selected>Token-based Chunking (Recommended)</option>
          <option value="scene_map">Scene Map Analysis (Advanced)</option>
        </select>
      </div>
      
      <button type="submit" class="btn btn-primary">
        <span class="btn-text">Analyze Keynote</span>
      </button>
      
      <div class="loading" id="loading">
        <div class="spinner"></div>
        <p>Processing your keynote... This may take a few minutes.</p>
      </div>
    </form>
    
    <div class="supported-formats">
      <h4>Supported Formats</h4>
      <div class="format-list">
        <span class="format-tag">.txt</span>
        <span class="format-tag">.md</span>
        <span class="format-tag">.docx</span>
        <span class="format-tag">.srt</span>
      </div>
    </div>
  </div>
</div>

<script>
document.getElementById('uploadForm').addEventListener('submit', function() {
  document.querySelector('.btn-text').textContent = 'Processing...';
  document.querySelector('.btn-primary').disabled = true;
  document.getElementById('loading').style.display = 'block';
});

// File input enhancement
document.getElementById('file').addEventListener('change', function(e) {
  const file = e.target.files[0];
  if (file) {
    const fileSize = (file.size / 1024 / 1024).toFixed(2);
    console.log(`Selected: ${file.name} (${fileSize} MB)`);
  }
});
</script>
</body>
</html>
"""

@app.post('/analyze', response_class=HTMLResponse)
async def analyze(file: UploadFile, strategy: Optional[str] = Form('tokens')):
    suffix = os.path.splitext(file.filename)[-1] or '.txt'
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    cfg = load_config('config.yaml')
    cfg['chunking']['strategy'] = strategy or 'tokens'
    run_cli(tmp_path, cfg)

    md_path = OUT_DIR / 'keynote_kfa.md'
    csv_path = OUT_DIR / 'keynote_kfa_notes.csv'
    md_preview = md_path.read_text(encoding='utf-8', errors='ignore')[:50000]

    def dl_link(p):
        return f"/download?path={urllib.parse.quote(str(p))}"

    return f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Analysis Results — Keynote KFA</title>
<style>
:root {{
  --primary: #2563eb;
  --primary-dark: #1d4ed8;
  --secondary: #64748b;
  --success: #059669;
  --background: #f8fafc;
  --surface: #ffffff;
  --border: #e2e8f0;
  --text: #1e293b;
  --text-muted: #64748b;
  --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --radius: 0.75rem;
}}

* {{
  box-sizing: border-box;
}}

body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: var(--text);
  background: var(--background);
  margin: 0;
  padding: 0;
  min-height: 100vh;
}}

.container {{
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}}

.header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}}

.back-link {{
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-muted);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}}

.back-link:hover {{
  color: var(--primary);
}}

.back-link::before {{
  content: "←";
  font-size: 1.2rem;
}}

h1 {{
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  color: var(--text);
}}

.success-badge {{
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--success);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  font-size: 0.875rem;
  font-weight: 600;
}}

.success-badge::before {{
  content: "✓";
  font-size: 1rem;
}}

.actions {{
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}}

.btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}}

.btn-primary {{
  background: var(--primary);
  color: white;
}}

.btn-primary:hover {{
  background: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}}

.btn-secondary {{
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
}}

.btn-secondary:hover {{
  background: var(--background);
  transform: translateY(-1px);
  box-shadow: var(--shadow-lg);
}}

.preview-container {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow);
}}

.preview-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: var(--background);
  border-bottom: 1px solid var(--border);
}}

.preview-title {{
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
  color: var(--text);
}}

.view-toggle {{
  display: flex;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  overflow: hidden;
}}

.toggle-btn {{
  padding: 0.5rem 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  border: none;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
}}

.toggle-btn.active {{
  background: var(--primary);
  color: white;
}}

.preview-content {{
  padding: 1.5rem;
  max-height: 70vh;
  overflow-y: auto;
}}

.markdown-content {{
  line-height: 1.7;
}}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {{
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: var(--text);
}}

.markdown-content h1 {{ font-size: 1.875rem; }}
.markdown-content h2 {{ font-size: 1.5rem; }}
.markdown-content h3 {{ font-size: 1.25rem; }}

.markdown-content p {{
  margin-bottom: 1rem;
}}

.markdown-content ul,
.markdown-content ol {{
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}}

.markdown-content li {{
  margin-bottom: 0.5rem;
}}

.markdown-content blockquote {{
  border-left: 4px solid var(--primary);
  padding-left: 1rem;
  margin: 1rem 0;
  color: var(--text-muted);
  font-style: italic;
}}

.markdown-content code {{
  background: var(--background);
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
}}

.markdown-content pre {{
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem;
  overflow-x: auto;
  margin: 1rem 0;
}}

.markdown-content pre code {{
  background: none;
  padding: 0;
}}

.raw-content {{
  display: none;
}}

.raw-content pre {{
  white-space: pre-wrap;
  background: var(--background);
  border: 1px solid var(--border);
  padding: 1rem;
  border-radius: var(--radius);
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
}}

@media (max-width: 768px) {{
  .container {{
    padding: 1rem;
  }}
  
  .header {{
    flex-direction: column;
    align-items: flex-start;
  }}
  
  .actions {{
    width: 100%;
  }}
  
  .btn {{
    flex: 1;
    justify-content: center;
  }}
  
  .preview-header {{
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }}
}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div>
      <a href="/" class="back-link">Back to Upload</a>
      <h1>Analysis Complete</h1>
    </div>
    <div class="success-badge">Processing Complete</div>
  </div>
  
  <div class="actions">
    <a class="btn btn-primary" href="{dl_link(md_path)}">
      📄 Download Markdown
    </a>
    <a class="btn btn-secondary" href="{dl_link(csv_path)}">
      📊 Download CSV Notes
    </a>
  </div>
  
  <div class="preview-container">
    <div class="preview-header">
      <h2 class="preview-title">Content Preview</h2>
      <div class="view-toggle">
        <button class="toggle-btn active" onclick="showRendered()">Rendered</button>
        <button class="toggle-btn" onclick="showRaw()">Raw Markdown</button>
      </div>
    </div>
    
    <div class="preview-content">
      <div id="rendered-content" class="markdown-content">
        {md_preview.replace('<', '&lt;').replace('>', '&gt;')}
      </div>
      <div id="raw-content" class="raw-content">
        <pre>{md_preview}</pre>
      </div>
    </div>
  </div>
</div>

<script>
function showRendered() {{
  document.getElementById('rendered-content').style.display = 'block';
  document.getElementById('raw-content').style.display = 'none';
  document.querySelectorAll('.toggle-btn')[0].classList.add('active');
  document.querySelectorAll('.toggle-btn')[1].classList.remove('active');
}}

function showRaw() {{
  document.getElementById('rendered-content').style.display = 'none';
  document.getElementById('raw-content').style.display = 'block';
  document.querySelectorAll('.toggle-btn')[0].classList.remove('active');
  document.querySelectorAll('.toggle-btn')[1].classList.add('active');
}}

// Simple markdown-to-HTML conversion for basic formatting
function renderMarkdown(text) {{
  return text
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>')
    .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*)\*/gim, '<em>$1</em>')
    .replace(/!\[([^\]]*)\]\(([^\)]*)\)/gim, '<img alt="$1" src="$2" />')
    .replace(/\[([^\]]*)\]\(([^\)]*)\)/gim, '<a href="$2">$1</a>')
    .replace(/\n$/gim, '<br />');
}}

// Apply basic markdown rendering
document.addEventListener('DOMContentLoaded', function() {{
  const renderedContent = document.getElementById('rendered-content');
  const rawText = `{md_preview}`;
  renderedContent.innerHTML = renderMarkdown(rawText);
}});
</script>
</body>
</html>"""

@app.get('/download')
def download(path: str):
    # Allow only files under ./out
    p = pathlib.Path(path).resolve()
    if OUT_DIR.resolve() not in p.parents and OUT_DIR.resolve() != p:
        return PlainTextResponse("Invalid path", status_code=400)
    if not p.exists():
        return PlainTextResponse("Not found", status_code=404)
    return FileResponse(str(p), filename=p.name)
