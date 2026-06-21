from pypalettes import load_palette


def get_colrs(palette_nm: str, colr_no: int | None = None):
    if colr_no is not None:
        palette = load_palette("Fun")
    else:
        palette = load_palette("Fun")
    return palette
