#!/usr/bin/env python3
"""Migliora le foto Vinted copiando il "look" della foto di riferimento.

Uso:  python3 migliora_foto.py cartella_foto_originali [cartella_uscita]

Per ogni foto: corregge esposizione e bilanciamento del bianco, trasferisce
i colori caldi della foto di riferimento, aggiunge contrasto e nitidezza,
ritaglia in formato 4:5 (1600x2000) come la vetrina.
Il capo NON viene ritoccato a parte: si applica la stessa correzione a tutta
la foto, quindi il colore reale del prodotto resta credibile.
"""
import sys, pathlib
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

QUI = pathlib.Path(__file__).parent
RIF = QUI / "riferimento" / "stile.png"
FORZA_COLORE = 0.75   # 0 = nessun trasferimento, 1 = colori identici al riferimento
USCITA = (1600, 2000) # 4:5

def srgb_to_lab(rgb):
    c = rgb / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    M = np.array([[0.4124, 0.3576, 0.1805],[0.2126, 0.7152, 0.0722],[0.0193, 0.1192, 0.9505]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16/116)
    L = 116 * f[..., 1] - 16
    a = 500 * (f[..., 0] - f[..., 1]); b = 200 * (f[..., 1] - f[..., 2])
    return np.stack([L, a, b], -1)

def lab_to_srgb(lab):
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    fy = (L + 16) / 116; fx = fy + a / 500; fz = fy - b / 200
    f = np.stack([fx, fy, fz], -1)
    xyz = np.where(f > 0.206893, f ** 3, (f - 16/116) / 7.787) * np.array([0.95047, 1.0, 1.08883])
    Mi = np.array([[3.2406, -1.5372, -0.4986],[-0.9689, 1.8758, 0.0415],[0.0557, -0.2040, 1.0570]])
    c = np.clip(xyz @ Mi.T, 0, 1)
    c = np.where(c > 0.0031308, 1.055 * c ** (1/2.4) - 0.055, 12.92 * c)
    return np.clip(c * 255, 0, 255)

def stats(lab):
    flat = lab.reshape(-1, 3)
    return flat.mean(0), flat.std(0) + 1e-6

def taglio_45(img):
    w, h = img.size; r = 4/5
    if w / h > r:
        nw = int(h * r); x = (w - nw) // 2; img = img.crop((x, 0, x + nw, h))
    else:
        nh = int(w / r); y = (h - nh) // 2; img = img.crop((0, y, w, y + nh))
    return img.resize(USCITA, Image.LANCZOS)

def migliora(path, rif_stats):
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    img = taglio_45(img)
    # esposizione/contrasto automatici leggeri (taglia 0.5% di estremi)
    img = ImageOps.autocontrast(img, cutoff=0.5, preserve_tone=True)
    lab = srgb_to_lab(np.asarray(img, dtype=np.float64))
    m, s = stats(lab); rm, rs = rif_stats
    nuovo = (lab - m) / s * rs + rm
    lab = lab * (1 - FORZA_COLORE) + nuovo * FORZA_COLORE
    img = Image.fromarray(lab_to_srgb(lab).astype(np.uint8))
    # curva a S morbida per profondita'
    x = np.arange(256) / 255.0
    curva = x + 0.22 * (x - x**2) * (2*x - 1)
    curva = np.clip(curva * 255, 0, 255).astype(np.uint8)
    img = img.point(list(curva) * 3)
    img = ImageEnhance.Contrast(img).enhance(1.03)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
    return img

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    src = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else src.parent / (src.name + "_pronte")
    out.mkdir(parents=True, exist_ok=True)
    rif = Image.open(RIF).convert("RGB")
    rif_stats = stats(srgb_to_lab(np.asarray(rif, dtype=np.float64)))
    files = sorted(p for p in src.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".heic", ".webp"})
    for p in files:
        migliora(p, rif_stats).save(out / (p.stem + ".jpg"), quality=93, optimize=True)
        print("ok", p.name)
    print(f"{len(files)} foto salvate in {out}")

if __name__ == "__main__":
    main()
