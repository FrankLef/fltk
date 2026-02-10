import matplotlib.colors as mcolors


def convert_hex_to_rgba(hex: str, alpha: float | None = None) -> str:
    """Convert hex to a string with rgba, for plotly.

    Plotly only accept 6-digit hex but pypalettes gives 8-digit hex.
    """
    rgba = list(mcolors.to_rgba(hex, alpha=alpha))
    rgba_str = map(str, rgba)
    color = "rgba(" + ",".join(rgba_str) + ")"
    return color
