from openeo.processes import array_element, array_create, sqrt
from wildfire_viz_helper import calc_enhanced_natural_colors


# base_arr = base map array as the template to create spatial ones for black color arrays
def black_arr(
    base_arr,
):
    spatial_ones = array_element(base_arr, 0) * 0 + 1

    black = array_create(
        [spatial_ones * 0.00, spatial_ones * 0.00, spatial_ones * 0.00]
    )
    return black


def naturalColorsCC_arr(brightness, band_B04, band_03, band_02, offset):
    arr = array_create(
        [
            sqrt(brightness * band_B04 + offset),  # red
            sqrt(brightness * band_03 + offset),  # green
            sqrt(brightness * band_02 + offset),  # blue
        ]
    )
    return arr


def naturalColors_arr(brightness, band_B04, band_B03, band_B02, offset):
    arr = array_create(
        [
            2.5 * brightness * band_B04 + offset,  # red
            2.5 * brightness * band_B03 + offset,  # green
            2.5 * brightness * band_B02 + offset,  # blue
        ]
    )
    return arr


def urban_arr(brightness, band_B12, band_B11, band_B04, offset):
    arr = array_create(
        [
            sqrt(brightness * band_B12 * 1.2 + offset),  # red
            sqrt(brightness * band_B11 * 1.4 + offset),  # green
            sqrt(brightness * band_B04 + offset),  # blue
        ]
    )
    return arr


def swir_arr(brightness, band_B12, band_B8A, band_B04, offset):
    arr = array_create(
        [
            sqrt(brightness * band_B12 + offset),  # red
            sqrt(brightness * band_B8A + offset),  # green
            sqrt(brightness * band_B04 + offset),  # blue
        ]
    )
    return arr


# # NIRBlue - skip, using colorblend


def classicFalse_arr(brightness, band_B08, band_B04, band_B03):
    arr = array_create(
        [band_B08 * brightness, band_B04 * brightness, band_B03 * brightness]
    )
    return arr


def nir_arr(brightness, band_B08):
    arr = array_create(
        [band_B08 * brightness, band_B08 * brightness, band_B08 * brightness]
    )
    return arr


def atmoPen_arr(brightness, band_B12, band_B11, band_B08):
    arr = array_create(
        [band_B12 * brightness, band_B11 * brightness, band_B08 * brightness]
    )
    return arr


def enhancedNaturalColors(
    natural_colors_corrected, natural_colors, urban_colors, brightness
):
    arr = array_create(
        [
            calc_enhanced_natural_colors(
                0, natural_colors_corrected, natural_colors, urban_colors, brightness
            ),
            calc_enhanced_natural_colors(
                1, natural_colors_corrected, natural_colors, urban_colors, brightness
            ),
            calc_enhanced_natural_colors(
                2, natural_colors_corrected, natural_colors, urban_colors, brightness
            ),
        ]
    )
    return arr


def manualCorrection_arr(
    base_arr, red_correction=0, green_correction=0, blue_correction=0
):
    spatial_ones = array_element(base_arr, 0) * 0 + 1

    arr = array_create(
        [
            spatial_ones * red_correction,
            spatial_ones * green_correction,
            spatial_ones * blue_correction,
        ]
    )

    r_corrected = array_element(base_arr, 0) + array_element(arr, 0)
    g_corrected = array_element(base_arr, 1) + array_element(arr, 1)
    b_corrected = array_element(base_arr, 2) + array_element(arr, 2)

    base_arr_corrected = array_create([r_corrected, g_corrected, b_corrected])

    return base_arr_corrected
