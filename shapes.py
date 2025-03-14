import svgwrite
import math
import numpy as np

# A4 paper size in mm (SVG units)
A4_WIDTH = 2100
A4_HEIGHT = 2970

def create_polygon(x, y, side_length, n_sides, flip=False):
    """
    Creates a regular polygon centered at (x, y) with given side length and number of sides.
    Returns a list of (x, y) points.
    """

    angle_at_center = (2*np.pi) / n_sides #The angle at the center of a single side segment
    angle_at_corner = (np.pi - angle_at_center) / 2  #The angle at the corner of the polygon
    radius = np.sqrt( (side_length*side_length) / ( 2 - 2 * np.cos(angle_at_center) ) )

    # print("center", math.degrees(angle_at_center))
    # print("corner", math.degrees(angle_at_corner))
    # print("cos", np.cos(angle_at_center))
    # print("height", height)

    #Roots of unity party!!
    if n_sides == 3:
        z = radius * np.exp(np.pi * 0.5j) #starting up
    elif n_sides == 4:
        z = radius * np.exp(np.pi * 0.25j) #starting right-up
    elif n_sides == 5 or n_sides == 6 or n_sides == 8:
        z = radius #starting right

        if flip:
            polygon_height = radius * np.sin(angle_at_corner)
            z=-z
            x = x+radius-polygon_height
    # elif n_sides == 8:
    #     z = radius * np.exp(np.pi * 0.125j)
    else:
        raise ValueError("n_sides not recognised")


    w = np.exp((2j * np.pi) / n_sides)

    points = []
    for i in range(n_sides):
        p = z*np.pow(w, i)
        points.append((p.real + x, p.imag + y))

    return (angle_at_center, angle_at_corner, radius,points)

def generate_tessellation(filename, n_sides, side_length):
    """
    Generates an SVG file with tessellating polygons.
    The function calculates how to tile them based on the given number of sides.
    """
    dwg = svgwrite.Drawing(filename, size=(f"{A4_WIDTH}", f"{A4_HEIGHT}"))
    (angle_at_center, angle_at_corner, radius, polygon) = create_polygon(0,0, side_length, n_sides)

    dx=0
    dy=0
    if n_sides == 3:
        dx = side_length
        dy = math.sqrt(3) * side_length / 2 #side_length * sin(60) = side_length * (sqrt3/2)
    elif n_sides == 4:
        dx = side_length
        dy = side_length
    elif n_sides == 5:
        back_width = radius * np.cos(angle_at_center * 0.5)
        dx = radius + back_width
        polygon_height = side_length * np.cos((np.pi/2) - angle_at_corner)
        dy = 2 * polygon_height
    elif n_sides == 6:
        dx = 2 * radius + side_length
        polygon_height = radius * np.sin(angle_at_corner)
        dy = polygon_height
    elif n_sides == 8:
        dx = 2*radius
        dy = 2*radius
    else:
        raise TypeError("n_sides bad")



    num_cols = int(A4_WIDTH / dx) + 2
    num_rows = int(A4_HEIGHT / dy) + 2

    for row in range(num_rows):
        for col in range(num_cols):
            if n_sides == 6:
                x = ((col - 1/8) * dx)
                y = ((row + 1/4) * dy)
            elif n_sides == 8:
                x = ((col - 2/6) * dx)
                y = ((row - 2/6) * dy)
            else:
                x = ((col - 1/4) * dx)
                y = ((row - 1/4) * dy)

            # Adjust hexagons to form a staggered grid
            if (n_sides == 3 or  n_sides == 6) and row % 2 == 1:
                x += dx / 2

            # if n_sides == 8:
            #     x -= dx /4
            #     y -= dy /4

            #Adjust pentagon
            flip = n_sides == 5 and col % 2 == 1

            (_, _, _, polygon) = create_polygon(x, y, side_length, n_sides, flip)
            dwg.add(dwg.polygon(polygon, stroke="black", fill="none"))

    dwg.save()

generate_tessellation("triangle.svg", n_sides=3, side_length=200)
generate_tessellation("square.svg", n_sides=4, side_length=200)
generate_tessellation("pentagon.svg", n_sides=5, side_length=200)
generate_tessellation("hexagon.svg", n_sides=6, side_length=200)
generate_tessellation("octogon.svg", n_sides=8, side_length=200)
