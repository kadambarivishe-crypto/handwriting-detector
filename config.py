"""Configuration settings"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    API_TITLE = "AI Handwriting Detector API"
    API_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False") == "True"
    MODEL_PATH = os.getenv("MODEL_PATH", "models/handwriting_model.h5")
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "bmp"}
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False