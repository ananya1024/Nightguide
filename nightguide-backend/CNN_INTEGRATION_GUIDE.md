# 🤖 CNN Integration Guide for NightGuide

This guide explains how to integrate your CNN model into the NightGuide constellation detection system.

## 📋 Overview

The NightGuide backend is designed to work with both traditional Computer Vision methods and CNN-based detection. The system automatically falls back to traditional methods if CNN is not available or fails.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI        │    │   CNN Model     │
│   (React)       │◄──►│   Backend        │◄──►│   (Your Model)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   Traditional    │
                       │   CV Methods     │
                       └──────────────────┘
```

## 🔧 Integration Steps

### 1. Prepare Your Model

Your CNN model should be saved in one of these formats:
- **TensorFlow**: `.h5` or `.pb` files
- **PyTorch**: `.pth` or `.pt` files  
- **ONNX**: `.onnx` files

### 2. Update Requirements

Uncomment the relevant ML library in `requirements.txt`:

```bash
# For TensorFlow
tensorflow==2.13.0

# For PyTorch
torch==2.0.1
torchvision==0.15.2

# For ONNX
onnxruntime==1.15.1
```

### 3. Implement CNN Integration

Edit `cnn_integration.py` and implement these methods:

#### A. Load Model
```python
def load_model(self, model_path: str) -> bool:
    try:
        if self.model_type == "tensorflow":
            import tensorflow as tf
            self.model = tf.keras.models.load_model(model_path)
        elif self.model_type == "pytorch":
            import torch
            self.model = torch.load(model_path, map_location='cpu')
            self.model.eval()
        elif self.model_type == "onnx":
            import onnxruntime as ort
            self.model = ort.InferenceSession(model_path)
        
        self.is_loaded = True
        return True
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        return False
```

#### B. Preprocess Image
```python
def preprocess_image(self, image: np.ndarray) -> np.ndarray:
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Resize to model input size
    resized = cv2.resize(image_rgb, (self.input_size, self.input_size))
    
    # Normalize pixel values (0-1)
    normalized = resized.astype(np.float32) / 255.0
    
    # Add batch dimension
    batched = np.expand_dims(normalized, axis=0)
    
    return batched
```

#### C. Run Inference
```python
def detect_constellations(self, image: np.ndarray) -> List[Dict]:
    if not self.is_loaded:
        return []
    
    try:
        # Preprocess
        processed = self.preprocess_image(image)
        
        # Run inference
        if self.model_type == "tensorflow":
            predictions = self.model.predict(processed)
        elif self.model_type == "pytorch":
            import torch
            with torch.no_grad():
                input_tensor = torch.from_numpy(processed).float()
                predictions = self.model(input_tensor)
                predictions = predictions.numpy()
        elif self.model_type == "onnx":
            predictions = self.model.run(None, {'input': processed})[0]
        
        # Process predictions
        return self._process_predictions(predictions, image.shape)
        
    except Exception as e:
        logger.error(f"Inference failed: {str(e)}")
        return []
```

#### D. Process Predictions
```python
def _process_predictions(self, predictions: np.ndarray, image_shape: Tuple[int, int, int]) -> List[Dict]:
    results = []
    
    # Example: predictions shape is [batch_size, num_constellations, 5]
    # where 5 = [confidence, x1, y1, x2, y2] for bounding box
    
    for pred in predictions[0]:  # First batch
        confidence = pred[0]
        if confidence > self.confidence_threshold:
            x1, y1, x2, y2 = pred[1:5]
            
            # Convert to relative coordinates
            h, w = image_shape[:2]
            x1_rel, y1_rel = x1 / w, y1 / h
            x2_rel, y2_rel = x2 / w, y2 / h
            
            # Map to constellation name (you'll need to implement this mapping)
            constellation_name = self._map_prediction_to_constellation(pred)
            
            results.append({
                "constellation": constellation_name,
                "confidence": float(confidence),
                "bbox": [x1_rel, y1_rel, x2_rel, y2_rel],
                "stars": self._extract_stars_from_bbox(x1_rel, y1_rel, x2_rel, y2_rel),
                "lines": self._get_constellation_lines(constellation_name)
            })
    
    return results
```

### 4. Configure Environment

Create a `.env` file in the backend directory:

```bash
# Enable CNN
USE_CNN=true

# Path to your model
CNN_MODEL_PATH=./models/your_constellation_model.h5

# Model configuration
MODEL_TYPE=tensorflow
MODEL_INPUT_SIZE=224
CONFIDENCE_THRESHOLD=0.8
```

### 5. Test Integration

```bash
# Start the backend
cd nightguide-backend
python run.py

# Check logs for CNN initialization
# Should see: "CNN detector initialized successfully"
```

## 📊 Expected Output Format

Your CNN should return predictions in this format:

```python
[
    {
        "constellation": "Orion",
        "confidence": 0.95,
        "bbox": [0.1, 0.2, 0.8, 0.9],  # [x1, y1, x2, y2] relative coordinates
        "stars": [
            {"x": 0.2, "y": 0.3, "name": "Betelgeuse"},
            {"x": 0.5, "y": 0.5, "name": "Mintaka"},
            # ... more stars
        ],
        "lines": [
            [0.2, 0.3, 0.5, 0.5],  # [x1, y1, x2, y2] for constellation lines
            # ... more lines
        ]
    }
]
```

## 🔍 Testing Your Integration

### 1. Unit Test
```python
# test_cnn.py
import numpy as np
from cnn_integration import CNNConstellationDetector

# Create test image
test_image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

# Test your detector
detector = CNNConstellationDetector("path/to/your/model.h5")
results = detector.detect_constellations(test_image)

print(f"Detected {len(results)} constellations")
for result in results:
    print(f"- {result['constellation']}: {result['confidence']:.2f}")
```

### 2. Integration Test
```bash
# Start backend with CNN enabled
USE_CNN=true CNN_MODEL_PATH=./your_model.h5 python run.py

# Upload test image via frontend or curl
curl -X POST "http://localhost:8000/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@test_image.jpg"
```

## 🐛 Troubleshooting

### Common Issues

1. **Model not loading**
   - Check file path and permissions
   - Verify model format compatibility
   - Check required dependencies

2. **Memory issues**
   - Reduce model input size
   - Use GPU if available
   - Implement batch processing

3. **Incorrect predictions**
   - Verify preprocessing matches training
   - Check coordinate system (relative vs absolute)
   - Validate confidence thresholds

### Debug Mode

Enable debug logging:
```bash
LOG_LEVEL=DEBUG python run.py
```

## 📈 Performance Optimization

1. **Model Optimization**
   - Use TensorRT for TensorFlow
   - Use TorchScript for PyTorch
   - Quantize model weights

2. **Inference Optimization**
   - Batch multiple images
   - Use GPU acceleration
   - Implement caching

3. **Memory Management**
   - Load model once at startup
   - Clear GPU memory after inference
   - Use model serving (TensorFlow Serving, TorchServe)

## 🤝 Support

If you encounter issues:
1. Check the logs for error messages
2. Verify your model format and preprocessing
3. Test with a simple image first
4. Ensure all dependencies are installed

The system will automatically fall back to traditional CV methods if CNN fails, so your integration won't break the existing functionality. 