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
FORZA_COLORE = 1.0   # intensita' dell'effetto oro sulla paglia (0 = nessuno)
STIRA = 0.7          # 0 = nessun effetto anti-pieghe, 1 = massimo
USCITA = (2160, 2700) # 4:5, larghezza 4K (2160 px)

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
    # porta sempre a 2160x2700; la nitidezza viene ridata dopo
    img = img.resize(USCITA, Image.LANCZOS)
    return img

def maschera_paglia(rgb):
    """Pixel giallo/oro (paglia), sfumati. Il capo grigio/scuro resta escluso."""
    hsv = np.asarray(Image.fromarray(rgb.astype(np.uint8)).convert("HSV"), dtype=np.float64)
    h = hsv[..., 0] * 360 / 255; s = hsv[..., 1] / 255; v = hsv[..., 2] / 255
    tono = np.clip(1 - np.abs(h - 38) / 22, 0, 1)        # arancio-giallo
    m = tono * np.clip((s - 0.18) / 0.15, 0, 1) * np.clip((v - 0.15) / 0.2, 0, 1)
    m = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))
    return np.asarray(m, dtype=np.float64)[..., None] / 255


def _box(a, r):
    """Box blur separabile (cumsum) su array 2D float."""
    if r < 1: return a
    p = np.pad(a, ((r + 1, r), (0, 0)), mode="edge"); c = np.cumsum(p, 0)
    a = (c[2 * r + 1:] - c[:-2 * r - 1]) / (2 * r + 1)
    p = np.pad(a, ((0, 0), (r + 1, r)), mode="edge"); c = np.cumsum(p, 1)
    return (c[:, 2 * r + 1:] - c[:, :-2 * r - 1]) / (2 * r + 1)

def _blur(a, sigma):
    r = max(1, int(round(sigma * 0.9)))
    for _ in range(3): a = _box(a, r)
    return a

def stira(rgb, paglia, forza=STIRA):
    """Attenua le pieghe: toglie le ombre "medie" (pieghe) dal tessuto
    lasciando la trama fine e i bordi/bottoni/finiture di colore diverso.
    Non cambia la forma del capo e non nasconde macchie piccole o difetti."""
    if forza <= 0: return rgb
    lab = srgb_to_lab(rgb); L = lab[..., 0]
    h, w = L.shape; sc = w / 1000.0
    capo = 1 - paglia[..., 0]
    # colore dominante del capo (zona centrale)
    cy, cx = slice(h // 4, 3 * h // 4), slice(w // 4, 3 * w // 4)
    sel = capo[cy, cx] > 0.8
    a0 = np.median(lab[cy, cx, 1][sel]); b0 = np.median(lab[cy, cx, 2][sel])
    d2 = (lab[..., 1] - a0) ** 2 + (lab[..., 2] - b0) ** 2
    simile = np.exp(-d2 / (2 * 9.0 ** 2)) * capo
    simile = np.where(L > 8, simile, 0)
    # blur normalizzato: solo pixel del tessuto principale
    def nblur(x, s):
        return _blur(x * simile, s) / (_blur(simile, s) + 1e-4)
    medio = nblur(L, 7 * sc)       # ombre delle pieghe + trama media
    base = nblur(L, 45 * sc)       # illuminazione generale del capo
    piega = np.clip(medio - base, -14, 14)
    lab[..., 0] = L - forza * piega * simile
    return lab_to_srgb(lab)

def migliora(path, rif_stats):
    img = taglio_45(ImageOps.exif_transpose(Image.open(path)).convert("RGB"))
    rgb = np.asarray(img, dtype=np.float64)

    # 1) esposizione: livelli automatici SOLO sulla luminosita' (i colori del
    #    capo non vengono saturati), poi luminosita' media verso il riferimento
    lab = srgb_to_lab(rgb)
    lo, hi = np.percentile(lab[..., 0], [0.3, 99.7])
    lo = min(lo, 12.0); hi = max(hi, 85.0)          # stretch moderato
    lab[..., 0] = np.clip((lab[..., 0] - lo) / (hi - lo) * 100, 0, 100)
    Lm = lab[..., 0].mean(); target = rif_stats[0][0]
    gamma = np.clip(np.log(max(target, 1) / 100) / np.log(max(Lm, 1) / 100), 0.80, 1.0)   # solo schiarire, mai scurire
    lab[..., 0] = 100 * (lab[..., 0] / 100) ** gamma
    rgb = lab_to_srgb(lab)

    # 2) paglia: calda, oro e viva come nel riferimento (solo lei, non il capo)
    m = maschera_paglia(rgb)
    lab = srgb_to_lab(rgb)
    oro = lab.copy()
    # adattivo: porta il colore medio della paglia verso quello del riferimento
    # (paglia spenta -> spinta forte, paglia gia' gialla -> spinta leggera)
    peso = m[..., 0]; tot = max(peso.sum(), 1)
    b_att = (lab[..., 2] * peso).sum() / tot
    a_att = (lab[..., 1] * peso).sum() / tot
    oro[..., 2] = lab[..., 2] * float(np.clip(45 / max(b_att, 1), 1.0, 1.6))
    oro[..., 1] = lab[..., 1] + max(0.0, 11 - a_att) * 0.7
    oro[..., 0] = lab[..., 0] * 1.03
    lab = lab * (1 - m * FORZA_COLORE) + oro * (m * FORZA_COLORE)
    rgb = stira(lab_to_srgb(lab), m)          # 2b) attenua le pieghe del tessuto
    img = Image.fromarray(rgb.astype(np.uint8))

    # 3) il capo resta del suo colore reale: saturazione globale minima
    img = ImageEnhance.Color(img).enhance(1.03)

    # 4) curva a S morbida + "chiarezza" (contrasto locale per trama e cuciture)
    x = np.arange(256) / 255.0
    curva = np.clip((x + 0.22 * (x - x**2) * (2*x - 1)) * 255, 0, 255).astype(np.uint8)
    img = img.point(list(curva) * 3)
    img = img.filter(ImageFilter.UnsharpMask(radius=35, percent=12, threshold=0))
    img = img.filter(ImageFilter.UnsharpMask(radius=2.2, percent=85, threshold=2))
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
        migliora(p, rif_stats).save(out / (p.stem + ".jpg"), quality=95, subsampling=0, optimize=True)
        print("ok", p.name)
    print(f"{len(files)} foto salvate in {out}")

if __name__ == "__main__":
    main()
