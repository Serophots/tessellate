import svgwrite
import math
import numpy as np

# A4 paper size in mm (SVG units)
A4_WIDTH = 2100
A4_HEIGHT = 2970

def to_point(c, x, y):
    return (c.real + x, c.imag + y)

def create_polygon(x, y, side_length):
    """
    Creates a regular polygon centered at (x, y) with given side length and number of sides.
    Returns a list of (x, y) points.
    """
    n_sides = 4
    angle_at_center = (2*np.pi) / n_sides #The angle at the center of a single side segment
    angle_at_corner = (np.pi - angle_at_center) / 2  #The angle at the corner of the polygon
    radius = np.sqrt( (side_length*side_length) / ( 2 - 2 * np.cos(angle_at_center) ) )

    # print("center", math.degrees(angle_at_center))
    # print("corner", math.degrees(angle_at_corner))
    # print("cos", np.cos(angle_at_center))
    # print("height", height)

    z = radius * np.exp(np.pi * 0.25j) #starting right-up


    w = np.exp((2j * np.pi) / n_sides)

    points = ([
        to_point(z, x, y),
        to_point(z * w, x, y),
        to_point(z * w * w, x, y),
    ],
    [
        to_point(z, x, y),
        to_point(z * w * w * w, x, y),
        to_point(z * w * w, x, y)
    ])

    return (angle_at_corner, radius, points)

def generate_tessellation(filename, side_length):
    """
    Generates an SVG file with tessellating polygons.
    The function calculates how to tile them based on the given number of sides.
    """
    dwg = svgwrite.Drawing(filename, size=(f"{A4_WIDTH}", f"{A4_HEIGHT}"))
    (angle_at_corner, radius, polygon) = create_polygon(0,0, side_length)

    dx = side_length
    dy = side_length

    num_cols = int(A4_WIDTH / dx) + 2
    num_rows = int(A4_HEIGHT / dy) + 2

    for row in range(num_rows):
        for col in range(num_cols):
            x = (col * dx)
            y = (row * dy)

            (_, _, (a,b)) = create_polygon(x, y, side_length)
            dwg.add(dwg.polygon(a, stroke="black", fill="none"))
            dwg.add(dwg.polygon(b, stroke="black", fill="none"))

    dwg.save()

generate_tessellation("right_triangle.svg", side_length=200)
