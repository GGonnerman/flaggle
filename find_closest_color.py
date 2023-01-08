import colorsys
from functools import cache
from PIL import ImageColor
from skimage import io, color
from colors import RGB_COLORS, HLS_COLORS

def convert_rgb_hls(color):
    r, g, b = color
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    return (h, l, s)

def convert_hls_rgb(color):
    h, l, s = color
    r, g, b = [round(x * 255) for x in colorsys.hls_to_rgb(h, l, s)]
    return (r, g, b)

def convert_rgb_lab(c):
    r, g, b = c
    return color.rgb2lab((r/255, g/255, b/255))

def convert_lab_rgb(c):
    r, g, b = [round(x * 255) for x in color.lab2rgb(c)]
    return (r, g, b)

# Get the similarity score of two colors in Lab color space
# Currently uses the delta E 2000 as described in 
# http://zschuessler.github.io/DeltaE/learn/
def get_score(color1, color2):
    return color.deltaE_ciede2000(color1, color2)

# A wrapper function to make it easier to test the find_closest_color function
def find_closest_rgb(r, g, b):
    return find_closest_color('#{:02x}{:02x}{:02x}'.format(r, g, b))

# Find the closest value to the hex value from a list of approved colors
# Has to be hex param so that caching works correctly
# Returns a tuple of (r, g, b)
@cache
def find_closest_color(hex):
    rgb = ImageColor.getcolor(hex, "RGB")

    destination = convert_rgb_lab(rgb)

    color_list = RGB_COLORS
    #color_list = HIS_COLORS
    #color_list = [convert_hls_rgb(c) for c in HLS_COLORS]

    lab_colors = [convert_rgb_lab(color) for color in color_list]
    
    lab_colors = sorted(lab_colors, key=lambda x: get_score(destination, x))

    closest_color = convert_lab_rgb(lab_colors[0])
    return closest_color

if __name__ == "__main__":
    pass
