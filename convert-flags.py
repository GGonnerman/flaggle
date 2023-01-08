import numpy as np
import os
import json
import requests
from time import sleep
from wand.image import Image as WandImage
from methodtools import lru_cache
from PIL import Image, ImageColor
from cairosvg import svg2png
from find_closest_color import find_closest_color

# Read image from input_path/name.svg and use cairosvg to export to
# a png at output_path/name.png
def convert_svg_to_png(input_path, output_path, name):
    with open(f"{input_path}/{name}.svg", "r") as flagsvg:
        svg_code = " ".join(flagsvg.readlines())

    svg2png(bytestring=svg_code, write_to=f"{output_path}/{name}.png")

# Limit a png (input_path/name.png) to a list of colors
# It attempts to convert each pixel to the closest match
# using Lab color space and the deltaE_cie76 method
def limit_colors(input_path, name):
    flag_image = Image.open(f"{input_path}/{name}.png")
    pixel_map = flag_image.load()
    width, height = flag_image.size

    for i in range(width):
        for j in range(height):

            pixel = flag_image.getpixel((i, j))

            # Ignore everything that is completely transparent
            if(len(pixel) == 4 and pixel[3] == 0):
                continue

            r, g, b = pixel[0:3]
            hex = rgb2hex( r, g, b )

            pixel_map[i, j] = ( find_closest_color(hex) )

    flag_image.save(f"{input_path}/{name}.png", format="png")

def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

# Remove unnecessary fields and remove countries whose flags have been
# excluded for various issues.
# Some nations (namely es- and gb-) will have to be added manually
def process_countries_json(block_list):

    with open("flag-icons/country.json", "r") as file:
        country_file = json.load(file)

    country_pairs = {}

    for country in country_file:
        name = country['name'].lower()
        code = country['code']

        if code in block_list: continue

        resp = requests.get(f"https://restcountries.com/v3.1/alpha/{code}")
        data = {}
        try:
            data = json.loads(resp.content)[0]
        except Exception as e:
            print(e)

        population = 0
        if 'population' in data: population = data['population']
        region = ''
        if 'region' in data: region = data['region']
        landlocked = ''
        if 'landlocked' in data: landlocked = data['landlocked']
        capital = ''
        if 'capital' in data: capital = data['capital'][0]

        country_pairs[name] = {
            "code": code,
            "population": population,
            "region": region,
            "landlocked": landlocked,
            "capital": capital,
        }

        print(name, country_pairs[name])

        sleep(15)

    with open("src/countries.json", "w") as file:
        json.dump(country_pairs, file)

# Loop through every svg in the input_path and output a corresponding
# png to the output_path while ignoring countries in the block_list
# Then limit the colors for each generated png
def convert_images(input_path, output_path, block_list):
    for flag in os.listdir(input_path):
        name = flag.split(".")[0]
        if name in block_list: continue
        print(name)
        convert_svg_to_png(input_path, output_path, name)
        limit_colors(output_path, name)

def check_color_list(input_path):
    unique_colors = set()
    for flag in os.listdir(input_path):
        flag_image = Image.open(f"{input_path}/{flag}")
        instances = flag_image.getcolors()
        for count, color in instances:
            if len(color) == 4: color = color[0:3]
            if color not in unique_colors:
                unique_colors.add(color)

    print("Unique Color List:", unique_colors)
    print("Number of Unique Colors:", len(unique_colors))

def check_duplicates(input_path):
    unique_flags = {}
    for flag in os.listdir(input_path):
        code = flag.split(".")[0]
        flag_sig = WandImage(filename=f"{input_path}/{flag}").signature

        if flag_sig not in unique_flags:
            unique_flags[flag_sig] = [code]
            print(flag)
        else:
            unique_flags[flag_sig].append(code)
            print(flag, " (duplicate)")

    pairs = list(filter(lambda x: len(x) > 1, unique_flags.values()))

    with open("src/pairs.json", "w") as file:
        json.dump(pairs, file)

if __name__ == "__main__":
    input_path = "flag-icons/flags/4x3"
    output_path = "assets/flags"

    # List of ignored flags (some break cairo)
    block_list = ["bs", "bo", "bz", "cefta", "ci", "cw", "dg", "do", "eu", "io", "lv", "pe", "qa", "rs", "th", "um", "un", "va", "xx", "re", "bl", "mt", "pg"]

    #convert_images(input_path, output_path, block_list)
    process_countries_json(block_list)
    #check_color_list(output_path)
    #check_duplicates(output_path)
