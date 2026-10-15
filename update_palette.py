# Add the colours used by assets/*.png to assets.pyxpal, one group per file.
# Existing colours keep their index, assets.pyxres refers to them.

# python3 update_palette.py
# .venv/bin/python update_palette.py

import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
PALETTE = ROOT / "assets.pyxpal"
MAX_COLORS = 256


def read_png(path):
    # Set of (r, g, b, a) found in an 8-bit, non-interlaced PNG.
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit(f"{path.name}: not a PNG")
    pos, idat, plte, trns = 8, [], b"", b""
    while pos < len(data):
        size, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + size]
        pos += 12 + size
        if kind == b"IHDR":
            w, h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", body)
        elif kind == b"IDAT":
            idat.append(body)
        elif kind == b"PLTE":
            plte = body
        elif kind == b"tRNS":
            trns = body
    if depth != 8 or interlace or ctype not in (0, 2, 3, 4, 6):
        sys.exit(f"{path.name}: only 8-bit non-interlaced PNG is supported")
    bpp = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    stride = w * bpp
    raw = zlib.decompress(b"".join(idat))
    found, prev = set(), bytes(stride)
    for y in range(h):
        i = y * (stride + 1)
        kind, row = raw[i], bytearray(raw[i + 1:i + 1 + stride])
        if kind == 1:
            for x in range(bpp, stride):
                row[x] = (row[x] + row[x - bpp]) & 255
        elif kind == 2:
            row = bytearray((a + b) & 255 for a, b in zip(row, prev))
        elif kind in (3, 4):
            for x in range(stride):
                a = row[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                if kind == 3:
                    row[x] = (row[x] + (a + b) // 2) & 255
                else:
                    pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                    row[x] = (row[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        elif kind != 0:
            sys.exit(f"{path.name}: bad PNG filter {kind}")
        prev = row
        if ctype == 6:
            found |= set(zip(row[0::4], row[1::4], row[2::4], row[3::4]))
        elif ctype == 2:
            found |= {(r, g, b, 255) for r, g, b in zip(row[0::3], row[1::3], row[2::3])}
        elif ctype == 0:
            found |= {(g, g, g, 255) for g in set(row)}
        elif ctype == 4:
            found |= {(g, g, g, a) for g, a in zip(row[0::2], row[1::2])}
        else:
            for n in set(row):
                found.add((*plte[n * 3:n * 3 + 3], trns[n] if n < len(trns) else 255))
    return found


def brightness(color):
    r, g, b = (int(color[i:i + 2], 16) for i in (0, 2, 4))
    return 0.299 * r + 0.587 * g + 0.114 * b


def ranges(indices):
    out = []
    for i in indices:
        if out and i == out[-1][1] + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return ", ".join(str(a) if a == b else f"{a}-{b}" for a, b in out)


def main():
    text = PALETTE.read_text() if PALETTE.exists() else "000000\n"
    pal = text.lower().split()
    start = len(pal)
    out = text.rstrip("\n") + "\n"
    report = []
    for png in sorted(ASSETS.glob("*.png")):
        pixels = read_png(png)
        colors = {"%02x%02x%02x" % p[:3] for p in pixels if p[3]}
        if any(p[:3] != (0, 0, 0) for p in pixels if not p[3]):
            print(f"{png.name}: transparent pixels are not black, pyxel draws them")
        new = sorted(colors - set(pal), key=brightness)
        if new:
            out += "\n" + "\n".join(new) + "\n"
            pal += new
        report.append(f"{png.name}: {ranges(sorted(i for i in map(pal.index, colors) if i))}")
    if len(pal) > MAX_COLORS:
        sys.exit(f"{len(pal)} colours, pyxel supports {MAX_COLORS}")
    print("\n".join(report))
    if len(pal) == start:
        print(f"{PALETTE.name}: up to date, {start} colours")
        return
    PALETTE.write_text(out)
    print(f"{PALETTE.name}: {len(pal)} colours (+{len(pal) - start})")


if __name__ == "__main__":
    main()
