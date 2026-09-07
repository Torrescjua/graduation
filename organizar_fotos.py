#!/usr/bin/env python3
"""
Organiza tus fotos y videos para la página de Daniela.

Qué hace:
1. Lee todas las imágenes y videos de una carpeta de origen (esa carpeta
   con todas tus fotos que "no puedes subir porque son muchas").
2. Las COPIA (nunca mueve ni borra el original) a la carpeta fotos/ de esta
   página, renombrándolas foto-001.jpg, foto-002.jpg... y video-001.mp4,
   video-002.mp4... en orden cronológico (por fecha de modificación).
3. Si tienes Pillow instalado (pip install pillow), además comprime y
   convierte cada foto a un JPG liviano (máx. 2000px de lado, calidad 82)
   para que la página cargue rápido en el celular de Daniela. Si no lo
   tienes, copia los archivos tal cual, sin comprimir.
4. Si el número de fotos/videos que encuentra es distinto al que ya tiene
   configurado index.html (76 fotos, 24 videos), imprime al final el bloque
   CONFIG actualizado para que lo pegues ahí.

Uso:
    python3 organizar_fotos.py /ruta/a/tu/carpeta/con/fotos

Requiere Python 3 (viene instalado en Mac y Linux; en Windows instala
python.org/downloads si no lo tienes).
"""
import sys
import shutil
from pathlib import Path

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif", ".bmp", ".tiff"}
VIDEO_EXT = {".mp4", ".mov", ".m4v"}

try:
    from PIL import Image, ImageOps
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 organizar_fotos.py /ruta/a/tu/carpeta/con/fotos")
        sys.exit(1)

    source = Path(sys.argv[1]).expanduser()
    if not source.is_dir():
        print(f"No encuentro esa carpeta: {source}")
        sys.exit(1)

    dest = Path(__file__).parent / "fotos"
    dest.mkdir(exist_ok=True)

    files = sorted(
        (f for f in source.iterdir() if f.is_file()),
        key=lambda f: f.stat().st_mtime,  # orden cronológico
    )
    photos = [f for f in files if f.suffix.lower() in IMAGE_EXT]
    videos = [f for f in files if f.suffix.lower() in VIDEO_EXT]

    print(f"Encontré {len(photos)} fotos y {len(videos)} videos en {source}\n")
    if not HAS_PIL:
        print("(Pillow no está instalado -> copio las fotos tal cual, sin comprimir.")
        print(" Para optimizarlas automáticamente: pip install pillow)\n")

    aspect_ratios = []
    for i, f in enumerate(photos, start=1):
        out_path = dest / f"foto-{i:03d}.jpg"
        if HAS_PIL:
            try:
                img = Image.open(f)
                img = ImageOps.exif_transpose(img)  # respeta la orientación real de la foto
                img = img.convert("RGB")
                max_side = 2000
                if max(img.size) > max_side:
                    ratio = max_side / max(img.size)
                    img = img.resize((int(img.width * ratio), int(img.height * ratio)))
                img.save(out_path, "JPEG", quality=82, optimize=True)
                aspect_ratios.append(f"{img.width}/{img.height}")
            except Exception as e:
                print(f"  ! No pude procesar {f.name} ({e}); la copio sin tocar.")
                shutil.copy2(f, out_path)
                aspect_ratios.append("4032/3024")
        else:
            shutil.copy2(f, out_path)
            aspect_ratios.append("4032/3024")
        print(f"  foto-{i:03d}.jpg  <-  {f.name}")

    for i, f in enumerate(videos, start=1):
        out_path = dest / f"video-{i:03d}.mp4"
        shutil.copy2(f, out_path)
        note = "  (ojo: es .mov, revisa que se reproduzca bien en el navegador)" if f.suffix.lower() != ".mp4" else ""
        print(f"  video-{i:03d}.mp4  <-  {f.name}{note}")

    print(f"\nListo. Copié {len(photos)} fotos y {len(videos)} videos a la carpeta fotos/.")

    print("\nSi este número es distinto al que ya tiene index.html (76 fotos, 24 videos),")
    print("pega esto dentro de CONFIG en index.html, reemplazando esas líneas:\n")
    print(f"    galleryCount: {len(photos)},")
    print("    photoAspectRatios: [")
    for i in range(0, len(aspect_ratios), 8):
        chunk = ", ".join(f'"{r}"' for r in aspect_ratios[i:i + 8])
        print(f"      {chunk},")
    print("    ],")
    print("    videoFiles: [")
    video_names = ", ".join(f'"video-{i:03d}.mp4"' for i in range(1, len(videos) + 1))
    print(f"      {video_names}")
    print("    ]")


if __name__ == "__main__":
    main()
