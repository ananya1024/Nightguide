import uvicorn
import os
from dotenv import load_dotenv
from config import Config

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Validate configuration
    Config.validate_cnn_config()
    Config.print_config()
    
    print(f"🚀 Starting NightGuide API on {Config.HOST}:{Config.PORT}")
    print(f"📖 API Documentation: http://{Config.HOST}:{Config.PORT}/docs")
    print(f"🔍 Health Check: http://{Config.HOST}:{Config.PORT}/health")
    
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True,  # Enable auto-reload for development
        log_level=Config.LOG_LEVEL.lower()
    ) 