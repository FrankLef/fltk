import matplotlib.pyplot as plt

from fltk.graphics.show_colrs import show_palettes


pal_nms = (
    "jetColors",
    "viridis",
    "magma",
    "plasma",
    "inferno",
    "cividis",
    "mako",
    "rocket",
    "turbo",
)


def main():
    fig = show_palettes(pal_nms)  # noqa: F841
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
