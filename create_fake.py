from PIL import Image
import piexif

def create_fake_document():
    # Create a simple dummy document image
    img = Image.new('RGB', (800, 600), color=(255, 255, 255))
    
    # 1. Add some "fake" content (a red box representing pasted text)
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([100, 100, 400, 200], fill=(200, 0, 0))
    
    # 2. Add a Photoshop EXIF signature to trigger the EXIF module
    exif_dict = {"0th": {piexif.ImageIFD.Software: b"Adobe Photoshop CC 2021"}}
    exif_bytes = piexif.dump(exif_dict)
    
    # Save the explicitly "forged" image
    img.save("forged_document.jpg", "jpeg", exif=exif_bytes)
    print("Created forged_document.jpg! Upload this to the playground.")

if __name__ == "__main__":
    create_fake_document()
