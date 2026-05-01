import base64
import cv2
import numpy as np
import io
from PIL import Image, ImageChops

def perform_ela(image_bytes: bytes, quality=90):
    try:
        original = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        temp_buffer = io.BytesIO()
        original.save(temp_buffer, format="JPEG", quality=quality)
        temp_buffer.seek(0)
        
        resaved = Image.open(temp_buffer).convert("RGB")
        
        ela_image = ImageChops.difference(original, resaved)
        
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        
        ela_array = np.array(ela_image)
        mean_diff = np.mean(ela_array)
        
        score = min((mean_diff * max_diff / 255.0) / 10.0, 1.0)
        
        gray = cv2.cvtColor(ela_array, cv2.COLOR_RGB2GRAY)
        cv2.normalize(gray, gray, 0, 255, cv2.NORM_MINMAX)
        heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
        
        _, buffer = cv2.imencode('.jpg', heatmap)
        base64_img = base64.b64encode(buffer).decode('utf-8')
        visual_proof = f"data:image/jpeg;base64,{base64_img}"
        
        return {
            "status": "success",
            "max_difference": float(max_diff),
            "mean_difference": float(mean_diff),
            "score": float(score),
            "visual_proof": visual_proof
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
