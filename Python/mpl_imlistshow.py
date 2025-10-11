import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def imlistshow(ax, imgs: list[np.ndarray], *args, **kwargs):
    imgs = imgs.copy()
    fig = ax.get_figure()
    curr_i = 0
    ax.imshow(imgs[0], *args, **kwargs)

    def keypress(event):
        nonlocal curr_i
        prev_map_i = curr_i

        if event.key in ("h", "left"):
            curr_i = (curr_i - 1) % len(imgs)
        elif event.key in ("l", "right"):
            curr_i = (curr_i + 1) % len(imgs)

        if prev_map_i != curr_i:
            ax.clear()
            ax.imshow(imgs[curr_i], *args, **kwargs)
            fig.canvas.draw_idle()
            fig.canvas.flush_events()

    fig.canvas.mpl_connect("key_press_event", keypress)


if __name__ == "__main__":
    img_exts = (".png", ".jpg", ".jpeg", ".bmp", ".webp")

    dir = sys.argv[1]
    img_paths = sorted(Path(dir).glob("*.*g"))
    img_paths = [p for p in img_paths if str(p).lower().endswith(img_exts)]
    imgs = [plt.imread(p) for p in img_paths]

    imlistshow(plt.gca(), imgs)
    plt.show()
