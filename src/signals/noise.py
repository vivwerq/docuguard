import cv2
import numpy as np

def calculate_noise_variance(image_bytes: bytes):
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        variance = laplacian.var()
        
        score = 0.0
        if variance < 100:
             score = 0.8
        elif variance > 3000:
             score = 0.6
             
        return {
            "status": "success",
            "variance": float(variance),
            "score": score
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
