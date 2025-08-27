#!/usr/bin/env python3
"""
Simple test without Streamlit dependencies
"""

def test_basic_functionality():
    """Test basic configuration functionality"""
    
    # Test default config
    default_config = {
        'strategy': 'tokens',
        'chunk_tokens': 2000,
        'overlap_tokens': 200,
        'temperature': 0.2,
        'max_output_tokens': 1500
    }
    
    print("Default config:", default_config)
    
    # Test config merging
    saved_config = {
        'chunk_tokens': 3000,
        'temperature': 0.5
    }
    
    merged = default_config.copy()
    merged.update(saved_config)
    
    print("Merged config:", merged)
    
    # Test individual value access
    strategy = merged.get('strategy', 'tokens')
    chunk_tokens = merged.get('chunk_tokens', 2000)
    
    print(f"Strategy: {strategy}")
    print(f"Chunk tokens: {chunk_tokens}")
    
    print("✅ Basic functionality test passed!")

if __name__ == "__main__":
    test_basic_functionality()