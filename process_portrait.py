import os
import sys

def main():
    print("Testing python environment...")
    try:
        from PIL import Image, ImageEnhance, ImageFilter, ImageOps
        print("PIL is available")
    except ImportError:
        print("PIL is NOT available")
        return

    src_path = os.path.join("assets", "profile.png")
    if not os.path.exists(src_path):
        print(f"Source not found: {src_path}")
        return

    with Image.open(src_path) as img:
        print(f"Image format: {img.format}, size: {img.size}, mode: {img.mode}")

    # Check rembg
    try:
        import rembg
        print("rembg is available!")
    except ImportError:
        print("rembg is NOT available")

if __name__ == "__main__":
    main()
