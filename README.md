# 🌌 NightGuide

AI-powered constellation identifier — upload a night-sky photo and get constellation overlays.  
Mono-repo with **frontend** (React + Vite + Tailwind) and **backend** (FastAPI + OpenCV).

## ✨ Features

- 📸 **Image Upload**: Upload night sky photos
- 🔍 **AI Analysis**: Detect stars and identify constellations
- 🎨 **Interactive Overlay**: Visual constellation lines and star points
- 📱 **Responsive Design**: Works on desktop and mobile
- ⚡ **Real-time Processing**: Fast analysis with loading states

## 🚀 Quickstart

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd nightguide-backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
python run.py
```

The backend will start on `http://localhost:8000`

### Frontend Setup

```bash
cd nightguide-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start on `http://localhost:5173`

## 🏗️ Project Structure

```
AstronomyHackathon/
├── nightguide-backend/
│   ├── main.py                 # FastAPI application
│   ├── constellation_detector.py # AI constellation detection
│   ├── requirements.txt        # Python dependencies
│   └── run.py                 # Backend startup script
├── nightguide-frontend/
│   ├── src/
│   │   ├── App.jsx            # Main application component
│   │   ├── components/
│   │   │   ├── ConstellationOverlay.jsx # Canvas overlay component
│   │   │   └── LoadingSpinner.jsx       # Loading animation
│   │   └── main.jsx           # React entry point
│   ├── package.json           # Node.js dependencies
│   └── vite.config.js         # Vite configuration
└── README.md                  # This file
```

## 🔧 API Endpoints

### Backend API (FastAPI)

- `GET /` - API info and endpoints
- `GET /health` - Health check
- `GET /constellations` - List available constellations
- `POST /upload` - Upload and analyze image

### Response Format

```json
{
  "constellation": "Orion",
  "description": "The Hunter",
  "lines": [[x1, y1, x2, y2], ...],
  "points": [{"x": 0.2, "y": 0.3, "name": "Betelgeuse"}, ...],
  "detected_stars": 15,
  "confidence": "high"
}
```

## 🎨 Frontend Components

### ConstellationOverlay
- Renders constellation lines and star points on canvas
- Supports custom styling and animations
- Responsive design

### LoadingSpinner
- Space-themed loading animation
- Customizable messages
- Smooth transitions

## 🛠️ Development

### Backend Development
- Uses OpenCV for image processing
- Hough Circle Transform for star detection
- Pattern matching for constellation identification
- FastAPI for REST API

### Frontend Development
- React 19 with hooks
- Tailwind CSS for styling
- Vite for fast development
- Canvas API for overlays

## 🚀 Deployment

### Backend Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Run with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Serve static files
npm run preview
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is part of the Astronomy Hackathon.

## 🌟 Future Enhancements

- [x] Real AI/ML constellation detection (CNN integration ready)
- [ ] Multiple constellation detection
- [ ] Star brightness analysis
- [ ] Mobile app version
- [ ] Social sharing features
- [ ] Constellation database expansion

## 🤖 CNN Integration

The backend is designed to work with CNN models for advanced constellation detection:

- **Hybrid Architecture**: Combines traditional CV with CNN detection
- **Automatic Fallback**: Falls back to traditional methods if CNN fails
- **Multiple Frameworks**: Supports TensorFlow, PyTorch, and ONNX
- **Easy Integration**: See `nightguide-backend/CNN_INTEGRATION_GUIDE.md` for details

### Quick CNN Setup:
```bash
# Enable CNN detection
USE_CNN=true CNN_MODEL_PATH=./your_model.h5 python run.py
```
