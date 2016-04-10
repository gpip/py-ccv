from PIL import Image, ImageDraw


def draw_rects(im, rects, save_to=None, **kwargs):
    """
    Draw rectangles over image. rects is assumed to be a list of ccv.Feature
    """
    draw = ImageDraw.Draw(im)
    params = {'fill': 'purple', 'width': 5}
    params.update(kwargs)
    for r in rects:
        box = [(r.x1, r.y1), (r.x1, r.y2),
               (r.x2, r.y2), (r.x2, r.y2),
               (r.x2, r.y1)]
        draw.line(box + [box[0]], **params)

    if save_to:
        im.save(save_to)
    return im


def draw_rects_from_file(filename, rects, save_to=None, **kwargs):
    """Same as draw_rects, but loads image from filename first."""
    im = Image.open(filename)
    return draw_rects(im, rects, save_to, **kwargs)
