#!/usr/bin/env python

from PIL import Image
import argparse
import csv

mi = 10000
ma = -10000


def map_range(value, start1, stop1, start2, stop2):
    normalized_value = (value - start1) / (stop1 - start1)
    mapped_value = start2 + normalized_value * (stop2 - start2)
    return mapped_value


parser = argparse.ArgumentParser(description="Simple CLI tool to convert the NASA ADC csv files to images. May be "
                                             "useful.")

parser.add_argument('part', help='The part to render to an image. Height, Longitude, Latitude, or Slope')
parser.add_argument('name', help='The name of the region in the file.')

args = parser.parse_args()

with open(f"NASA ADC/Data/FY23_ADC_{args.part}_{args.name}.csv") as data:
    csv_reader = csv.reader(data)

    y = 0

    for i in csv_reader:
        x = 0
        for j in i:
            if float(j) < mi:
                mi = float(j)
            if float(j) > ma:
                ma = float(j)
            x += 1
        y += 1

with open(f"NASA ADC/Data/FY23_ADC_{args.part}_{args.name}.csv") as data:
    csv_reader = csv.reader(data)

    width, height = x, y

    y = 0

    image = Image.new('F', (width, height))

    for i in csv_reader:
        x = 0
        for j in i:
            image.putpixel((x, y), map_range(float(j), mi, ma, 0, 1))
            x += 1
        y += 1

image.save(args.name.lower() + "_" + args.part.lower() + ".tif")
