from PIL import Image, ExifTags
import io

SUSPICIOUS_SOFTWARE = ["adobe", "photoshop", "gimp", "canva", "lightroom", "pixelmator"]

def analyze_exif(image_bytes: bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        exif_data = image.getexif()
        
        if not exif_data:
            return {
                "status": "success",
                "has_exif": False,
                "score": 0.8,
                "reason": "Missing EXIF data (common in screenshots or completely re-exported files)",
                "metadata": {}
            }
        
        metadata = {}
        suspicious_software_found = None
        
        for tag_id, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            if isinstance(value, bytes):
                try:
                    value = value.decode('utf-8', errors='ignore')
                except:
                    value = str(value)
            
            metadata[tag_name] = value
            
            if tag_name in ['Software', 'ProcessingSoftware', 'HostComputer']:
                value_lower = str(value).lower()
                for software in SUSPICIOUS_SOFTWARE:
                    if software in value_lower:
                        suspicious_software_found = str(value)
                        break

        score = 0.9 if suspicious_software_found else 0.0
        reason = f"Suspicious editing software detected: {suspicious_software_found}" if suspicious_software_found else "No suspicious software signatures found"
        
        return {
            "status": "success",
            "has_exif": True,
            "score": score,
            "reason": reason,
            "metadata": metadata
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
