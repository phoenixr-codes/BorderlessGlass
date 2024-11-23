from PIL import Image
from pathlib import Path
import os
from collections import Counter

type Color = tuple[int, int, int]


def dominant_color(im: Image) -> Color:
    return (Counter(im.getdata()).most_common(1))[0][0]


def main():
    prebuild = Path(os.environ["ALLAY_PREBUILD"])
    colors: dict[str, Color] = {}

    for file in prebuild.glob("**/*glass*.png"):
        if "pane" in file.stem:
            continue
        im = Image.open(file)
        new_border_color = dominant_color(im)
        color_name = file.stem.removeprefix("glass")
        colors[color_name] = new_border_color
        for h in range(im.height):
            for w in range(im.width):
                if w == 0 or w == im.width - 1 or h == 0 or h == im.height - 1:
                    # print((w, h), new_border_color)
                    im.putpixel((w, h), new_border_color)
        im.save(file)

    for file in prebuild.glob("**/glass_pane*.png"):
        color_name = file.stem.removeprefix("glass_pane_top")
        im = Image.new(mode="RGBA", size=(1, 1), color=colors[color_name])
        im.save(file)


if __name__ == "__main__":
    main()
