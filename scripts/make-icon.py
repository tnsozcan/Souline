"""Generate the Souline app icon (assets/souline.ico and assets/souline.png).

A rounded square with a violet-to-blue gradient and a speaker dot sending three
sound waves. Drawn at 1024 px and downscaled so every size stays sharp.
"""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SIZE = 1024


def gradient(size: int) -> Image.Image:
    top, bottom = (139, 92, 246), (37, 99, 235)  # violet -> blue
    img = Image.new("RGBA", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * (size - 1))
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)) + (255,)
    return img


def make_icon() -> Image.Image:
    base = gradient(SIZE)
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, SIZE - 1, SIZE - 1), radius=230, fill=255)
    icon = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    icon.paste(base, (0, 0), mask)

    draw = ImageDraw.Draw(icon)
    white = (255, 255, 255, 255)
    cx, cy = 330, SIZE // 2
    draw.ellipse((cx - 95, cy - 95, cx + 95, cy + 95), fill=white)  # speaker dot
    width = 70
    for radius in (250, 400, 550):
        box = (cx - radius, cy - radius, cx + radius, cy + radius)
        draw.arc(box, start=-45, end=45, fill=white, width=width)
    return icon


def main() -> None:
    icon = make_icon()
    assets = ROOT / "assets"
    icon.resize((256, 256), Image.LANCZOS).save(assets / "souline.png")
    icon.save(assets / "souline.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("assets/souline.ico, assets/souline.png")


if __name__ == "__main__":
    main()
