#!/usr/bin/env python3
"""
Simple test for configuration memory functionality
"""
from kfa.config_manager import ConfigManager

def test_localStorage():
    """Test localStorage functionality"""
    print("Testing localStorage...")
    
    # Create config manager
    config_manager = ConfigManager(storage_type="localStorage")
    
    # Test default config
    default_config = config_manager.get_merged_config()
    print(f"Default config: {default_config}")
    
    # Test saving config
    test_config = {
        'strategy': 'scene_map',
        'chunk_tokens': 3000,
        'temperature': 0.5
    }
    
    config_manager.save_config(test_config)
    print(f"Saved config: {test_config}")
    
    # Test loading config
    loaded_config = config_manager.load_config()
    print(f"Loaded config: {loaded_config}")
    
    # Test merged config
    merged_config = config_manager.get_merged_config()
    print(f"Merged config: {merged_config}")
    
    # Test individual values
    strategy = config_manager.get_value('strategy')
    chunk_tokens = config_manager.get_value('chunk_tokens')
    print(f"Strategy: {strategy}, Chunk tokens: {chunk_tokens}")
    
    print("✅ localStorage test completed!\n")

def test_config_manager():
    """Test ConfigManager functionality"""
    print("Testing ConfigManager...")
    
    # Test localStorage
    storage_type = "localStorage"
    print(f"\n--- Testing {storage_type} storage ---")
    
    config_manager = ConfigManager(storage_type=storage_type)
    
    # Test saving and loading
    test_data = {
        'strategy': 'tokens',
        'chunk_tokens': 2500,
        'overlap_tokens': 300,
        'temperature': 0.3,
        'max_output_tokens': 2000
    }
    
    config_manager.save_config(test_data)
    loaded = config_manager.load_config()
    
    assert loaded == test_data, f"Config mismatch: {loaded} != {test_data}"
    print(f"✅ {storage_type} storage working correctly")
    
    # Test individual value access
    assert config_manager.get_value('strategy') == 'tokens'
    assert config_manager.get_value('chunk_tokens') == 2500
    print(f"✅ Individual value access working")
    
    # Test clearing
    config_manager.clear_config()
    cleared = config_manager.load_config()
    print(f"After clear: {cleared}")

if __name__ == "__main__":
    test_localStorage()
    test_config_manager()
    print("🎉 All tests passed!")