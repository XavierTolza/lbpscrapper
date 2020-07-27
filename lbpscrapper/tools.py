from io import BytesIO

import imageio


def element_screenshot_to_numpy(element):
    fp = BytesIO(element.screenshot_as_png)
    im = imageio.imread(fp)
    return im