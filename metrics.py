#!/usr/bin/python3
from PIL import Image
from tools import *
from operator import itemgetter

PATH='maps'
def proportion(map_image, mapName="", disp=False):
    """ Evaluate blurring of the map based on number_of_occupied_pixels/number_of_state-know_pixels.
    A high proportion, compared to another map, mean blurred walls ; thus, not clear map.
    That's a criteria, only considering wall blurring. It's not THE criteria.
    To determine if a pixel is free or a wall, we look if he is > (free) or < (wall) to pixels mean.
    Sometimes, wall thickness/blurring is not relevant of quality
    (error in loop closure -> generating big map -> lot of free space compared to wall generation -> great proportion...)

    Ref : 2D SLAM Quality Evaluation Methods
    https://arxiv.org/pdf/1708.02354.pdf """

    # Computation of pixels mean value
    valSum = 0
    valNbr = 0
    pix = map_image.load()
    for x in range(map_image.size[0]):
        for y in range(map_image.size[1]):
            val = pix[x, y]
            if val != 205 and val != 128:  # not unknown
                valSum += val
                valNbr += 1
    mean = valSum / valNbr

    # Number computation of wall and free-space pixels
    wallNbr = 0
    freeNbr = 0

    for x in range(map_image.size[0]):
        for y in range(map_image.size[1]):
            val = pix[x, y]
            if val != 205 and val != 128:  # not unknown
                if val < mean:
                    wallNbr += 1
                else:
                    freeNbr += 1

    # Proportion computation
    prop = wallNbr / float((wallNbr + freeNbr))
    if disp:
        if mapName != "":
            mapName += " : "
        print(mapName + str(prop) + "% of wall")

    return (prop)


def main():

    lesStats = []
    for mapName in get_files_names('.pgm', PATH):
        # Load image data
        map_image = getImage(mapName, PATH)

        # Proportion computation
        prop = proportion(map_image, mapName)

        # Map stats writing
        lesStats.append([mapName, prop])

        # Display proportion-ranked stats
        lesStatsPropRk = sorted(lesStats, key=itemgetter(1))
    print("proportion ranked : " + str(lesStatsPropRk))


main()
