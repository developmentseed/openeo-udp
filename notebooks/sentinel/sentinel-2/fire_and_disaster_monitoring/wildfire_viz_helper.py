from openeo.processes import and_, array_element, array_create, constant, eq


def not_(x):
    """Logical NOT using backend-supported processes (eq, constant)."""
    return eq(x, constant(False))


def or_(x, y):
    """Logical OR using backend-supported processes (eq, constant, and_)."""
    return eq(and_(eq(x, constant(False)), eq(y, constant(False))), constant(False))


def stretch(arr, min, max):
    """
    Linearly stretch RGB channels of an array between a minimum and maximum value.

    Each channel is rescaled using \((x - \\text{min}) / (\\text{max} - \\text{min})\)
    and the three stretched channels are returned as a new array.

    Parameters
    ----------
    arr:
        Array-like structure containing at least three bands representing R, G, B.
    min:
        Lower bound of the input value range used for stretching.
    max:
        Upper bound of the input value range used for stretching.

    Returns
    -------
    ArrayLike
        Array-like RGB structure with contrast-enhanced channels.
    """
    r = array_element(arr, 0)
    g = array_element(arr, 1)
    b = array_element(arr, 2)

    r_stretch = (r - min) / (max - min)
    g_stretch = (g - min) / (max - min)
    b_stretch = (b - min) / (max - min)

    return array_create([r_stretch, g_stretch, b_stretch])


def satEnh(arr, s):
    """
    Enhance or reduce saturation of an RGB array by mixing with its per-pixel mean.

    A saturation factor of 1 keeps the original colors, 0 converts to grayscale,
    and values in between interpolate linearly.

    Parameters
    ----------
    arr:
        Array-like structure containing at least three bands representing R, G, B.
    s:
        Saturation factor where 0 yields grayscale and 1 keeps original colors.

    Returns
    -------
    ArrayLike
        Array-like RGB structure with adjusted saturation.
    """
    r = array_element(arr, 0)
    g = array_element(arr, 1)
    b = array_element(arr, 2)

    avg = (r + g + b) / 3

    # Apply saturation formula to each channel
    r_sat = avg * (1 - s) + r * s
    g_sat = avg * (1 - s) + g * s
    b_sat = avg * (1 - s) + b * s

    return array_create([r_sat, g_sat, b_sat])


# Calculate enhanced natural colors by averaging true color and color-corrected
# renderings, then adding a subtle urban/SWIR tint for better contrast
def calc_enhanced_natural_colors(
    index,
    naturalColors_arr,
    naturalColorsCC_arr,
    urban_arr,
    brightness,
):
    """
    Compute an enhanced natural-color value for a given array index.

    The result is the average of the natural-color and color-corrected arrays
    at the given index, scaled by a brightness factor and lightly tinted by
    the corresponding urban/SWIR value.

    Parameters
    ----------
    index:
        Position of the band/RGB channel within the input arrays.
    naturalColors_arr:
        Array-like structure containing natural-color values.
    naturalColorsCC_arr:
        Array-like structure containing color-corrected natural-color values.
    urban_arr:
        Array-like structure used to provide an urban/SWIR tint.
    brightness:
        Multiplicative brightness factor applied to the averaged natural colors.

    Returns
    -------
    Any
        Enhanced natural-color value at the specified index.
    """
    natural = array_element(naturalColors_arr, index)
    naturalCC = array_element(naturalColorsCC_arr, index)
    urb = array_element(urban_arr, index)
    return brightness * ((natural + naturalCC) / 2) + (urb / 10)


# Blend three RGB layers using weighted opacity values
def layer_blend(
    layer1,
    layer2,
    layer3,
    opacity1,
    opacity2,
    opacity3,
):
    """
    Blend each RGB channel from three color arrays using per-layer opacity
    values expressed in percent.

    Parameters
    ----------
    layer1:
        First color array as an array-like structure with three bands (e.g. RGB).
    layer2:
        Second color array as an array-like structure with three bands (e.g. RGB).
    layer3:
        Third color array as an array-like structure with three bands (e.g. RGB).
    opacity1:
        Opacity of `layer1` in percent (0–100).
    opacity2:
        Opacity of `layer2` in percent (0–100).
    opacity3:
        Opacity of `layer3` in percent (0–100).

    Returns
    -------
    ArrayLike
        Array-like RGB structure representing the blended layers.
    """
    op1, op2, op3 = opacity1 / 100, opacity2 / 100, opacity3 / 100

    r = (
        (array_element(layer1, 0) * op1)
        + (array_element(layer2, 0) * op2)
        + (array_element(layer3, 0) * op3)
    )
    g = (
        (array_element(layer1, 1) * op1)
        + (array_element(layer2, 1) * op2)
        + (array_element(layer3, 1) * op3)
    )
    b = (
        (array_element(layer1, 2) * op1)
        + (array_element(layer2, 2) * op2)
        + (array_element(layer3, 2) * op3)
    )

    return array_create([r, g, b])


def isCloud(band_B03, band_B04):
    """
    Detect cloud pixels using the Normalized Green-Red Difference (NGDR)
    and a brightness ratio threshold.

    Parameters
    ----------
    band_B03:
        Green band value (Sentinel-2 Band 3, 559.8 nm)

    band_B04:
        Red band value (Sentinel-2 Band 4, 664.6 nm)

    Notes
    -----
    The function uses two criteria:
    - NGDR (Normalized Green-Red Difference): (B03 - B04) / (B03 + B04)
    - bRatio: brightness ratio normalizing B03 between 0.175 and 0.39

    A pixel is classified as cloud if:
    - bRatio > 1 (i.e., B03 > 0.39), OR
    - bRatio > 0 AND NGDR > 0 (i.e., B03 > 0.175 AND B03 > B04)
    """
    NGDR = (band_B03 - band_B04) / (band_B03 + band_B04)
    bRatio = (band_B03 - 0.175) / (0.39 - 0.175)
    return or_(bRatio > 1, and_(bRatio > 0, NGDR > 0))
