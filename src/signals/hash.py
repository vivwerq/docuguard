import imagehash
from PIL import Image
import io

def calculate_dhash(image_bytes: bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        hash_value = imagehash.dhash(img)
        return {
            "status": "success",
            "hash": str(hash_value)
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
