# Configuration Memory System

## Overview
The Keynote KFA application now remembers user configuration parameters using browser localStorage. Settings are automatically saved when changed and persist across browser sessions.

## Features

### ✅ Auto-Save Configuration
- **Chunk Size (tokens)**: 500-4000, default 2000
- **Overlap (tokens)**: 50-500, default 200  
- **AI Temperature**: 0.0-1.0, default 0.2
- **Max Output Tokens**: 500-3000, default 1500
- **Processing Strategy**: tokens/scene_map, default tokens

### ✅ Persistent Storage
- Uses browser **cookies** for persistence (100 days)
- Settings survive browser restarts
- Settings persist for 100 days or until manually cleared
- No server-side storage required

### ✅ Clean UX
- No manual save/reset buttons needed
- Settings auto-save on every change
- Seamless user experience
- Values restored on page load

## Implementation

### Core Components

1. **ConfigManager** (`kfa/config_manager.py`)
   - Unified interface for configuration management
   - Supports multiple storage backends
   - Handles defaults and merging

2. **Session Storage** (`kfa/session_storage.py`)
   - Streamlit session state storage
   - For temporary settings during session

3. **Persistent Storage** (`kfa/persistent_storage.py`)
   - Browser localStorage implementation
   - JavaScript components for browser interaction

4. **Cookie Storage** (`kfa/cookie_storage.py`)
   - Cookie-based storage option
   - 30-day expiration by default

### Usage

```python
from kfa.config_manager import ConfigManager, create_config_sidebar

# Initialize with cookies (100 days)
config_manager = ConfigManager(storage_type="cookie")

# Create sidebar with auto-save
user_config = create_config_sidebar(config_manager)

# Use configuration values
strategy = user_config['strategy']
chunk_tokens = user_config['chunk_tokens']
```

## Files Modified

- `app.py` - Updated to use ConfigManager with cookies
- `kfa/config_manager.py` - Main configuration management
- `kfa/session_storage.py` - Session-based storage
- `kfa/persistent_storage.py` - localStorage implementation  
- `kfa/cookie_storage.py` - Cookie-based storage
- `demo_config.py` - Demo application
- `test_config.py` - Test suite

## Testing

Run the test suite:
```bash
python test_config.py
```

Run the demo:
```bash
streamlit run demo_config.py
# or
streamlit run cookie_demo.py
```

## Benefits

1. **User Experience**: Settings remembered for 100 days
2. **No Backend**: Pure client-side cookie storage
3. **Functional Style**: Small, focused functions
4. **Auto-Save**: No manual intervention required
5. **Reliable**: Cookie-based persistence works across browser sessions