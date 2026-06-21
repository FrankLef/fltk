import matplotlib.pyplot as plt

from fltk.graphics.show_colrs import show_palettes

# "Noto Sans Display"

pal_nms = (
    "Tableau_10",
    "Tableau_20",
    "Classic_Cyclic",
    "Classic_10",
    "Classic_20",
    "Rainbow",
    "Traffic",
    "Vivid",
    "ink",
    "appletv",
    "excel_Atlas",
)


def main():
    fig = show_palettes(pal_nms)  # noqa: F841
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
