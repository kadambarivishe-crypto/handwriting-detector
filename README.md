# AI Handwriting Detector Backend

A FastAPI-based backend for detecting handwriting in images using machine learning.

## Features

- ✅ Image upload and processing
- ✅ Handwriting detection inference
- ✅ Batch processing support
- ✅ Docker containerization
- ✅ Health checks and monitoring
- ✅ CORS support
- ✅ Error handling and logging

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- TensorFlow 2.14+

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/kadambarivishe-crypto/handwriting-detector.git
cd handwriting-detector
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

5. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Docker Setup

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /health
```
Returns the health status and model loading state.

### Detect Handwriting
```
POST /detect
```
Detects handwriting in a single image.

**Parameters:**
- `file` (multipart/form-data): Image file

**Response:**
```json
{
  "status": "success",
  "filename": "image.png",
  "handwriting_detected": true,
  "confidence": 0.95,
  "predictions": {
    "handwritten": 0.95,
    "not_handwritten": 0.05
  }
}
```

### Batch Detect
```
POST /batch-detect
```
Detects handwriting in multiple images.

**Parameters:**
- `files` (multipart/form-data): Multiple image files

**Response:**
```json
{
  "status": "success",
  "total_files": 3,
  "results": [
    {
      "filename": "image1.png",
      "handwriting_detected": true,
      "confidence": 0.92
    },
    ...
  ]
}
```

### Model Info
```
GET /model-info
```
Returns information about the loaded model.

## Usage Examples

### Using cURL

```bash
# Single image detection
curl -X POST -F "file=@image.png" http://localhost:8000/detect

# Batch detection
curl -X POST -F "files=@image1.png" -F "files=@image2.png" http://localhost:8000/batch-detect

# Health check
curl http://localhost:8000/health
```

### Using Python

```python
import requests

# Single image
files = {'file': open('image.png', 'rb')}
response = requests.post('http://localhost:8000/detect', files=files)
print(response.json())

# Batch detection
files = [('files', open(f'image{i}.png', 'rb')) for i in range(1, 4)]
response = requests.post('http://localhost:8000/batch-detect', files=files)
print(response.json())
```

## Model Setup

Place your trained handwriting detection model at:
```
models/handwriting_model.h5
```

The model should be a TensorFlow/Keras model that:
- Accepts images of shape (224, 224, 1) - grayscale
- Outputs a single probability value between 0 and 1
- Returns values > 0.5 for handwritten content

## Configuration

Edit `.env` file to configure:
- `DEBUG`: Enable debug mode
- `MODEL_PATH`: Path to the ML model
- `MAX_UPLOAD_SIZE`: Maximum file upload size in bytes

## Project Structure

```
handwriting-detector/
├── main.py                 # FastAPI application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── models/               # ML models directory
    └── handwriting_model.h5
```

## Development

To run the server in development mode with hot reload:
```bash
uvicorn main.py:app --reload
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please create an issue on GitHub.