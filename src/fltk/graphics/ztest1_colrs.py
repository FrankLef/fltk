import matplotlib.pyplot as plt
from pypalettes import load_palette

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
    "Viridis",
    "jetColors",
)


def show_palettes(pal_nms):
    pal_len = len(pal_nms)

    # Set up the figure and axes for subplots
    fig, axes = plt.subplots(nrows=pal_len, figsize=(8, 2 * pal_len))

    for i, name in enumerate(pal_nms):
        ax = axes[i]

        # Load the palette (returns a list of colors)
        palette = load_palette(name)
        ncolrs = len(palette)

        # Create horizontal color bars
        for j, color in enumerate(palette):
            ax.barh(y=1, width=1, left=j, color=color, edgecolor="none")

        # Format the subplot
        ax.set_title(name, loc="left", fontsize=12, fontweight="bold", pad=4)
        ax.set_xlim(0, ncolrs)
        ax.set_ylim(0.5, 1.5)
        ax.axis("off")  # Hide axes to show only the color strip

    return fig


def main():
    fig = show_palettes(pal_nms)  # noqa: F841
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
