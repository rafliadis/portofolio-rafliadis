import os
import sys

def main():
    print("=" * 60)
    print("  EDITORIAL PORTRAIT GENERATOR (Alex Graham Style)")
    print("  Memproses assets/profile.png -> Cutout B&W High Contrast")
    print("=" * 60)

    # 1. Pastikan Pillow terinstall
    try:
        from PIL import Image, ImageEnhance, ImageOps, ImageFilter
        print("[✓] Pillow terpasang.")
    except ImportError:
        print("[!] Memasang Pillow...")
        os.system(f'"{sys.executable}" -m pip install Pillow')
        from PIL import Image, ImageEnhance, ImageOps, ImageFilter

    src_path = os.path.join("assets", "profile.png")
    backup_path = os.path.join("assets", "profile_original_beach.png")

    if not os.path.exists(src_path):
        print(f"[X] File {src_path} tidak ditemukan!")
        return

    # Backup file asli jika belum dibackup
    orig_img = Image.open(src_path)
    w, h = orig_img.size
    print(f"[*] Dimensi foto asli: {w} x {h}")

    if not os.path.exists(backup_path):
        orig_img.save(backup_path)
        print(f"[✓] Backup foto asli disimpan di: {backup_path}")

    # 2. Crop Portrait Editorial (Head & Shoulders / Dada ke Kepala)
    # Koordinat Rafli pada 2160x3840:
    left = int(w * 0.21)    # ~453 px
    top = int(h * 0.25)     # ~960 px (ruang di atas rambut)
    right = int(w * 0.79)   # ~1706 px
    bottom = int(h * 0.63)  # ~2419 px (baju hitam / dada bawah)

    crop_box = (left, top, right, bottom)
    print(f"[*] Melakukan cropping portrait: {crop_box} ({right-left}x{bottom-top} px)...")
    cropped = orig_img.crop(crop_box)

    # 3. AI Background Removal menggunakan rembg
    cutout = None
    try:
        import rembg
        print("[*] Menjalankan AI background removal (rembg)...")
        cutout = rembg.remove(cropped)
        print("[✓] Background berhasil dihapus dengan presisi AI!")
    except ImportError:
        print("[!] Paket 'rembg' belum terpasang. Mencoba menginstall otomatis...")
        ret = os.system(f'"{sys.executable}" -m pip install rembg onnxruntime')
        if ret == 0:
            try:
                import rembg
                print("[*] Menjalankan AI background removal (rembg)...")
                cutout = rembg.remove(cropped)
                print("[✓] Background berhasil dihapus dengan presisi AI!")
            except Exception as e:
                print(f"[!] Error saat eksekusi rembg: {e}")
        else:
            print("[!] Gagal memasang rembg secara otomatis.")

    # Fallback jika rembg tidak tersedia
    if cutout is None:
        print("[!] Menggunakan hasil crop dengan format RGBA...")
        cutout = cropped.convert("RGBA")

    # 4. Grading Black & White Editorial (High Contrast Alex Graham Style)
    print("[*] Menerapkan grading Black & White Editorial...")

    if cutout.mode != "RGBA":
        cutout = cutout.convert("RGBA")

    r, g, b, alpha = cutout.split()
    rgb = Image.merge("RGB", (r, g, b))

    # Konversi ke Grayscale bernuansa sinematik
    gray = ImageOps.grayscale(rgb)

    # Tingkatkan Kontras agar rambut & kaos hitam pekat, kulit cerah
    enhancer_con = ImageEnhance.Contrast(gray)
    high_con = enhancer_con.enhance(1.48)

    # Tingkatkan sedikit kecerahan highlight
    enhancer_bri = ImageEnhance.Brightness(high_con)
    bright = enhancer_bri.enhance(1.06)

    # Ketajaman detail tekstur
    enhancer_sha = ImageEnhance.Sharpness(bright)
    sharp = enhancer_sha.enhance(1.30)

    # Gabungkan kembali dengan Alpha Channel transparan
    final_portrait = Image.merge("RGBA", (sharp, sharp, sharp, alpha))

    # Resize proporsional agar ringan & tajam untuk web (lebar 1000px)
    target_w = 1000
    target_h = int(target_w * (final_portrait.height / final_portrait.width))
    final_portrait = final_portrait.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # 5. Simpan Hasil
    out_cutout = os.path.join("assets", "profile_cutout.png")
    out_profile = os.path.join("assets", "profile.png")

    final_portrait.save(out_cutout, "PNG", optimize=True)
    final_portrait.save(out_profile, "PNG", optimize=True)

    print("=" * 60)
    print("[✓] BERHASIL! Foto editorial tersimpan di:")
    print(f"    1. {out_cutout}")
    print(f"    2. {out_profile}")
    print("=" * 60)
    print("Buka index.html di browser untuk melihat hasilnya!")

if __name__ == "__main__":
    main()
