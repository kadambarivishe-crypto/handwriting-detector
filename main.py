from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from PIL import Image
import io
import tensorflow as tf
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Handwriting Detector API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model
model = None
MODEL_PATH = "models/handwriting_model.h5"

@app.on_event("startup")
async def startup_event():
    """Load the ML model on startup"""
    global model
    try:
        if Path(MODEL_PATH).exists():
            model = tf.keras.models.load_model(MODEL_PATH)
            logger.info("Model loaded successfully")
        else:
            logger.warning(f"Model not found at {MODEL_PATH}. Please ensure the model file exists.")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post("/detect")
async def detect_handwriting(file: UploadFile = File(...)):
    """
    Detect handwriting in an uploaded image
    
    Args:
        file: Image file (JPG, PNG, etc.)
    
    Returns:
        Detection results with confidence scores
    """
    try:
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Read and validate image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Preprocess image
        image = image.convert('L')  # Convert to grayscale
        image = image.resize((224, 224))  # Resize to model input size
        image_array = np.array(image) / 255.0  # Normalize
        image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
        
        # Run inference
        predictions = model.predict(image_array, verbose=0)
        confidence = float(predictions[0][0])
        
        # Prepare response
        return {
            "status": "success",
            "filename": file.filename,
            "handwriting_detected": confidence > 0.5,
            "confidence": confidence,
            "predictions": {
                "handwritten": confidence,
                "not_handwritten": 1 - confidence
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

@app.post("/batch-detect")
async def batch_detect(files: list[UploadFile] = File(...)):
    """
    Detect handwriting in multiple images
    
    Args:
        files: List of image files
    
    Returns:
        List of detection results
    """
    try:
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        results = []
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            image = image.convert('L')
            image = image.resize((224, 224))
            image_array = np.array(image) / 255.0
            image_array = np.expand_dims(image_array, axis=0)
            
            predictions = model.predict(image_array, verbose=0)
            confidence = float(predictions[0][0])
            
            results.append({
                "filename": file.filename,
                "handwriting_detected": confidence > 0.5,
                "confidence": confidence
            })
        
        return {
            "status": "success",
            "total_files": len(files),
            "results": results
        }
    
    except Exception as e:
        logger.error(f"Error in batch processing: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error in batch processing: {str(e)}")

@app.get("/model-info")
async def model_info():
    """Get information about the loaded model"""
    if model is None:
        return {"status": "error", "message": "Model not loaded"}
    
    return {
        "status": "success",
        "model_type": str(type(model)),
        "input_shape": model.input_shape,
        "output_shape": model.output_shape,
        "total_params": model.count_params()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)