import os
from typing import Optional

class Config:
    """Configuration management for NightGuide backend"""
    
    # Server settings
    PORT = int(os.getenv("PORT", 8000))
    HOST = os.getenv("HOST", "0.0.0.0")
    
    # CNN Model settings
    USE_CNN = os.getenv("USE_CNN", "false").lower() == "true"
    CNN_MODEL_PATH = os.getenv("CNN_MODEL_PATH")
    MODEL_TYPE = os.getenv("MODEL_TYPE", "tensorflow")  # tensorflow, pytorch, onnx
    MODEL_INPUT_SIZE = int(os.getenv("MODEL_INPUT_SIZE", 224))
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.8))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate_cnn_config(cls) -> bool:
        """Validate CNN configuration"""
        if cls.USE_CNN and not cls.CNN_MODEL_PATH:
            print("⚠️  Warning: USE_CNN=true but CNN_MODEL_PATH not set")
            return False
        
        if cls.CNN_MODEL_PATH and not os.path.exists(cls.CNN_MODEL_PATH):
            print(f"⚠️  Warning: CNN model file not found: {cls.CNN_MODEL_PATH}")
            return False
        
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration"""
        print("🌌 NightGuide Configuration:")
        print(f"  Server: {cls.HOST}:{cls.PORT}")
        print(f"  CNN Enabled: {cls.USE_CNN}")
        if cls.USE_CNN:
            print(f"  CNN Model: {cls.CNN_MODEL_PATH}")
            print(f"  Model Type: {cls.MODEL_TYPE}")
            print(f"  Input Size: {cls.MODEL_INPUT_SIZE}")
            print(f"  Confidence Threshold: {cls.CONFIDENCE_THRESHOLD}")
        print(f"  Log Level: {cls.LOG_LEVEL}") 