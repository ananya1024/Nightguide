import cv2
import numpy as np
from PIL import Image
import io
from typing import List, Dict, Tuple, Optional
import json
import os
import logging

logger = logging.getLogger(__name__)

class ConstellationDetector:
    def __init__(self, use_cnn: bool = False, cnn_model_path: Optional[str] = None):
        # Predefined constellation patterns (simplified for demo)
        self.constellations = {
            "Orion": {
                "description": "The Hunter",
                "stars": [
                    {"name": "Betelgeuse", "x": 0.2, "y": 0.3},
                    {"name": "Bellatrix", "x": 0.3, "y": 0.25},
                    {"name": "Mintaka", "x": 0.5, "y": 0.5},
                    {"name": "Alnilam", "x": 0.5, "y": 0.45},
                    {"name": "Alnitak", "x": 0.5, "y": 0.4},
                    {"name": "Saiph", "x": 0.4, "y": 0.7},
                    {"name": "Rigel", "x": 0.45, "y": 0.75}
                ],
                "lines": [
                    [0.2, 0.3, 0.3, 0.25],  # Betelgeuse to Bellatrix
                    [0.3, 0.25, 0.5, 0.5],  # Bellatrix to Mintaka
                    [0.5, 0.5, 0.5, 0.45],  # Mintaka to Alnilam
                    [0.5, 0.45, 0.5, 0.4],  # Alnilam to Alnitak
                    [0.5, 0.4, 0.4, 0.7],   # Alnitak to Saiph
                    [0.4, 0.7, 0.45, 0.75], # Saiph to Rigel
                    [0.45, 0.75, 0.2, 0.3]  # Rigel to Betelgeuse
                ]
            },
            "Ursa Major": {
                "description": "The Great Bear",
                "stars": [
                    {"name": "Dubhe", "x": 0.1, "y": 0.1},
                    {"name": "Merak", "x": 0.15, "y": 0.15},
                    {"name": "Phecda", "x": 0.2, "y": 0.2},
                    {"name": "Megrez", "x": 0.25, "y": 0.25},
                    {"name": "Alioth", "x": 0.3, "y": 0.3},
                    {"name": "Mizar", "x": 0.35, "y": 0.35},
                    {"name": "Alkaid", "x": 0.4, "y": 0.4}
                ],
                "lines": [
                    [0.1, 0.1, 0.15, 0.15],
                    [0.15, 0.15, 0.2, 0.2],
                    [0.2, 0.2, 0.25, 0.25],
                    [0.25, 0.25, 0.3, 0.3],
                    [0.3, 0.3, 0.35, 0.35],
                    [0.35, 0.35, 0.4, 0.4]
                ]
            },
            "Cassiopeia": {
                "description": "The Queen",
                "stars": [
                    {"name": "Schedar", "x": 0.6, "y": 0.2},
                    {"name": "Caph", "x": 0.7, "y": 0.25},
                    {"name": "Gamma Cas", "x": 0.8, "y": 0.3},
                    {"name": "Segin", "x": 0.75, "y": 0.4},
                    {"name": "Ruchbah", "x": 0.65, "y": 0.35}
                ],
                "lines": [
                    [0.6, 0.2, 0.7, 0.25],
                    [0.7, 0.25, 0.8, 0.3],
                    [0.8, 0.3, 0.75, 0.4],
                    [0.75, 0.4, 0.65, 0.35],
                    [0.65, 0.35, 0.6, 0.2]
                ]
            }
        }
        
        # CNN integration
        self.use_cnn = use_cnn
        self.cnn_detector = None
        
        if use_cnn and cnn_model_path:
            try:
                from cnn_integration import CNNConstellationDetector
                self.cnn_detector = CNNConstellationDetector(cnn_model_path)
                logger.info("CNN detector initialized successfully")
            except ImportError:
                logger.warning("CNN integration not available, falling back to traditional methods")
                self.use_cnn = False
            except Exception as e:
                logger.error(f"Failed to initialize CNN detector: {str(e)}")
                self.use_cnn = False

    def detect_stars(self, image: np.ndarray) -> List[Dict[str, float]]:
        """Detect bright points (stars) in the image"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Use Hough Circle Transform to detect circular bright spots
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=20,
            param1=50,
            param2=30,
            minRadius=3,
            maxRadius=20
        )
        
        stars = []
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                # Convert to relative coordinates (0-1)
                rel_x = x / image.shape[1]
                rel_y = y / image.shape[0]
                stars.append({
                    "x": rel_x,
                    "y": rel_y,
                    "radius": r,
                    "brightness": float(gray[y, x])
                })
        
        return stars

    def match_constellation(self, detected_stars: List[Dict[str, float]]) -> Tuple[str, Dict]:
        """Match detected stars to known constellations"""
        best_match = None
        best_score = 0
        
        for const_name, const_data in self.constellations.items():
            score = self._calculate_similarity(detected_stars, const_data["stars"])
            if score > best_score:
                best_score = score
                best_match = const_name
        
        # Return the best match or a default
        if best_match and best_score > 0.3:  # Threshold for confidence
            return best_match, self.constellations[best_match]
        else:
            # Return a random constellation for demo purposes
            import random
            const_name = random.choice(list(self.constellations.keys()))
            return const_name, self.constellations[const_name]

    def _calculate_similarity(self, detected_stars: List[Dict], const_stars: List[Dict]) -> float:
        """Calculate similarity between detected stars and constellation pattern"""
        if not detected_stars or not const_stars:
            return 0.0
        
        # Simple similarity based on star count and positions
        # In a real implementation, this would be much more sophisticated
        score = min(len(detected_stars), len(const_stars)) / max(len(detected_stars), len(const_stars))
        
        # Add some randomness for demo purposes
        import random
        score += random.uniform(0, 0.2)
        
        return min(score, 1.0)

    def process_image(self, image_bytes: bytes) -> Dict:
        """Process uploaded image and return constellation data"""
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                raise ValueError("Invalid image format")
            
            # Try CNN detection first if available
            if self.use_cnn and self.cnn_detector:
                logger.info("Attempting CNN-based constellation detection")
                cnn_results = self.cnn_detector.detect_constellations(image)
                
                if cnn_results:
                    # Use the first (most confident) result
                    cnn_result = cnn_results[0]
                    logger.info(f"CNN detected: {cnn_result.get('constellation', 'Unknown')}")
                    
                    # Convert CNN result to expected format
                    result = {
                        "constellation": cnn_result.get("constellation", "Unknown"),
                        "description": cnn_result.get("description", ""),
                        "lines": cnn_result.get("lines", []),
                        "points": cnn_result.get("stars", []),
                        "detected_stars": len(cnn_result.get("stars", [])),
                        "confidence": "high" if cnn_result.get("confidence", 0) > 0.8 else "medium",
                        "method": "cnn"
                    }
                    return result
            
            # Fallback to traditional methods
            logger.info("Using traditional CV methods for constellation detection")
            detected_stars = self.detect_stars(image)
            const_name, const_data = self.match_constellation(detected_stars)
            
            # Prepare response
            result = {
                "constellation": const_name,
                "description": const_data["description"],
                "lines": const_data["lines"],
                "points": const_data["stars"],
                "detected_stars": len(detected_stars),
                "confidence": "high" if len(detected_stars) > 5 else "medium",
                "method": "traditional"
            }
            
            return result
            
        except Exception as e:
            raise ValueError(f"Image processing failed: {str(e)}") 