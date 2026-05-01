import cv2
import numpy as np

def check_structure(image_bytes: bytes):
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        h, w = img.shape[:2]
        aspect_ratio = float(w) / h if h != 0 else 0
        
        score = 0.0
        reasons = []
        
        if 1.4 < aspect_ratio < 1.7:
             pass
        else:
             score = 0.4
             reasons.append(f"Non-standard aspect ratio ({aspect_ratio:.2f})")
             
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blur, 75, 200)
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        
        has_clear_edges = False
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                has_clear_edges = True
                break
                
        if not has_clear_edges:
             score += 0.3
             reasons.append("No clear rectangular document boundaries found")
             
        return {
            "status": "success",
            "aspect_ratio": aspect_ratio,
            "has_clear_edges": has_clear_edges,
            "score": min(score, 1.0),
            "reasons": reasons
        }
    except Exception as e:
         return {"status": "error", "error": str(e)}
