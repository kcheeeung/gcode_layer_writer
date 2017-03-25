from __future__ import division
import json
import os
import numpy as np
from skimage import color as skcolor
from skimage import io as skio
import matplotlib.pyplot as plt
from scipy.misc import imresize
from mpl_toolkits.mplot3d import Axes3D
import warnings
import functools
import itertools

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning) #turn off filter 
        warnings.warn("Call to deprecated function {}.".format(func.__name__), category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning) #reset filter
        return func(*args, **kwargs)

    return new_func


### CONSTANTS

MATERIAL_1 = "material 1"
MATERIAL_2 = "material 2"
MATERIAL_3 = "material 3"

# noop material
MATERIAL_NOOP = "noop"

# color map for visualizing print
COLOR_MAP = {MATERIAL_1: 'r', MATERIAL_2: 'g', MATERIAL_3: 'b'}

###

class GCommand(object):
    """Class representing a single action of the a microvalve"""

    def __init__(self, x, y, z, material, usecs=100):
        """
        Init

        x, x location in gcode coords
        y, y location in gcode coords
        z, z location in gcode coords
        material, material indicator
        usecs, delay after movement
        """
        self.x = x
        self.y = y
        self.z = z
        self.material = material
        self.usecs = usecs
    
    def __str__(self):
        """Returns gcode representation of command"""
        if self.material == MATERIAL_1:
            return "T0; G0 E10; G1 X{} Y{} ;material: {}\nM400 ;wait for position\nG4 P100\nM430 S{} ;send pulse\n"\
            .format(self.x, self.y, self.material, self.usecs)
        elif self.material == MATERIAL_2:
            return "T1; G0 E20; G1 X{} Y{} ;material: {}\nM400 ;wait for position\nG4 P100\nM430 S{} ;send pulse\n"\
            .format(self.x, self.y, self.material, self.usecs)
        elif self.material == MATERIAL_3:
            return "T2; G0 E30; G1 X{} Y{} ;material: {}\nM400 ;wait for position\nG4 P100\nM430 S{} ;send pulse\n"\
            .format(self.x, self.y, self.material, self.usecs)
        elif self.material == MATERIAL_NOOP:
            return ""

        raise ValueError("Unknown material: {}".format(self.material))


def write_json(filename):
    """
    Write a json config

    filename, path to write to
    """
    data = {"x":0, "y":0, "z":0, "heatbed_temp":37, "usecs": 100, "unitsize":1, "folder":"test_layers"}
    with open(filename, "w") as fp:
        json.dump(data, fp)

def load_json(filename):
    """
    Load a json config

    filename, path to load

    return data, dictionary object with config
    """
    with open(filename, "r") as fp:
        data = json.load(fp)
    x = data["x"]
    y = data["y"]
    z = data["z"]
    heatbed_temp = data["heatbed_temp"]
    usecs = data["usecs"]
    unitsize = data["unitsize"]
    return data

def load_raw_images(folder_path, check_dims=True):
    """
    Load images in raw form

    folder_path, path to folder with images
    check_dims, boolean to assert that all images have the same size

    return
    images, list of ndarrays of dimension height x width x 3 (color channels)
    paths, image paths
    """
    images = []
    paths = []

    for image_path in sorted(os.listdir(folder_path)):
        try:
            image = skio.imread(os.path.join(folder_path, image_path))
            images.append(image)
            paths.append(image_path)
        except Exception:
            print("{} cannot be opened".format(image_path))

    if check_dims:
        assert all((image.shape == images[0].shape for image in images)), "images do not have equal dimensions"
    
    return images, paths

@deprecated
def convert_to_binary(images):
    """
    Flatten images to black and white. This function is useful for testing
    but should be avoided.

    images, list of ndarrays of dimension height x width x 3 (color channels)

    return binarys, list of ndarrays of dimension height x width (elements are 0 or 1)
    """
    grays = [skcolor.rgb2gray(image) for image in images]
    binarys = []

    for image in grays:
        binary = image.copy().astype(np.uint8)
        binary[image <= 0.5] = 1
        binary[image > 0.5] = 0
        binarys.append(binary)

    return binarys

@deprecated
def resize_images(images, size):
    """
    Resize images. Useful for testing but deprecated as this makes designing unpredictable

    images, list of ndarrays
    size, desired size

    return list of resized images
    """
    return [imresize(image, size) for image in images]

def convert_to_gcode(binary_layers, usecs=600, grid_unit=0.5, z_unit=1.0, start_x=40, start_y=50, flip_flop=True):
    """
    Convert a list of binary images to gcommands. Iterates over each pixel
    and forms a GCommand object

    binary_layers, list of ndarrays of dimension height x width (elements are 0 or 1)
    usecs, delay for GCommand
    grid_unit, conversion of pixel to gcode dimensions in x and y
    z_unit, conversion of pixel to gcode dimensions in z
    start_x, start x location in gcode
    start_y, start y location in gcode
    flip_flop, boolean flip scans of left and right to minimize tracking

    return gcommand_layers, list of lists of GCommand objects
    """
    gcommand_layers = []

    for grid_z in range(len(binary_layers)):
        gcommands = []

        for grid_y in range(binary_layers[grid_z].shape[0]):
            if grid_y % 2 == 0 and flip_flop:
                x_iterator = reversed(range(binary_layers[grid_z].shape[1]))
            else:
                x_iterator = range(binary_layers[grid_z].shape[1])
            for grid_x in x_iterator:
                pixel = binary_layers[grid_z][grid_y, grid_x]
                material = convert_to_material(pixel)

                if material is not MATERIAL_NOOP:
                    gcommand = GCommand(grid_x * grid_unit + start_x, \
                                        grid_y * grid_unit + start_y, \
                                        grid_z * z_unit, \
                                        material, \
                                        usecs)
                    gcommands.append(gcommand)

        gcommand_layers.append(gcommands)

    return gcommand_layers

def convert_to_material(pixel):
    """
    Convert pixel color to printer material

    pixel, (r, g, b) ndarray slice

    return material constant if possible, otherwise ignore and print warning
    """
    red = pixel[0]
    green = pixel[1]
    blue = pixel[2]
    if (red, green, blue) == (255, 255, 255):
        return MATERIAL_NOOP
    if red == 255:
        return MATERIAL_1
    if green == 255:
        return MATERIAL_2
    if blue == 255:
        return MATERIAL_3
    else:
        print("Unrecognized color: (r: {}, g: {}, b: {})".format(red, green, blue))

def write_gcode(gcommand_layers, gcode_path, layer_names=None, heatbed_temp=37):
    """
    Convert list of gcommands into .gcode file. Also add start and end commands

    gcommand_layers, list of lists of GCommand objects
    gcode_path, path to write output
    layer_names, names for each layer, defaults to one index naming
    heatbed_temp, start temp UNUSED
    """
    assert heatbed_temp <= 200, "{} > max temp 200".format(heatbed_temp)

    if layer_names is not None:
        assert len(layer_names) == len(gcommand_layers), \
                "not enough names for all layers, remove layer_names to default naming"

    start_gcode = 'M42 P4 S250\n'
    end_gcode = 'M42 P4 S255\n'

    with open(gcode_path, 'w') as gcode_file:
        gcode_file.write(start_gcode)
        
        for layer_index, gcommands in enumerate(gcommand_layers):
            layer_name = layer_index + 1 if layer_names is None \
                            else layer_names[layer_index]
            gcode_file.write(";layer: {}\n".format(layer_name))

            for gcommand in gcommands:
                gcode_file.write(str(gcommand))
        
        gcode_file.write(end_gcode)

def graph(gcommand_layers, label_layers=False, layer_names=None, \
            grid_unit=None, z_unit=None, start_x=None, start_y=None, \
            color_map=COLOR_MAP, title="Print Preview"):
    """
    Graph gcommands in 3d. Also put layer names at each location if flagged

    gcommand_layers, list of lists of GCommand objects
    label_layers, boolean to label layers, requires additional args
    layer_names, names for each layer, if None don't label layers
    grid_unit, conversion of pixel to gcode dimensions in x and y
    z_unit, conversion of pixel to gcode dimensions in z
    start_x, start x location in gcode
    start_y, start y location in gcode
    color_map, mapping from material to color name string arg
    title, title for graph
    """
    if label_layers:
        assert grid_unit is not None, "if naming layers, need grid_unit"
        assert z_unit is not None, "if naming layers, need z_unit"
        assert start_x is not None, "if naming layers, need start_x"
        assert start_y is not None, "if naming layers, need start_y"
        if layer_names is not None:
            assert len(layer_names) == len(gcommand_layers), \
                    "not enough names for all layers, remove layer_names to default naming"

    gcommands = list(itertools.chain.from_iterable(gcommand_layers))

    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')
    materials = set((gcommand.material for gcommand in gcommands))
    split_on_materials = dict(((material, []) for material in materials))

    for gcommand in gcommands:
        split_on_materials[gcommand.material].append(gcommand)

    if color_map is None:
        from matplotlib import colors as cnames
        from itertools import cycle
        color_names = [name for name in cnames.cnames]
        color_names.sort()
        colors = cycle(color_names)
        color_map = dict(zip(materials, colors))

    for material, split in \
        sorted([(material, split) for (material, split) \
        in split_on_materials.items() if material is not MATERIAL_NOOP]):
        xs = [gcommand.x for gcommand in split]
        ys = [gcommand.y for gcommand in split]
        zs = [gcommand.z for gcommand in split]
        ax.scatter(xs, ys, zs, c=color_map[material], label=material)

    xmin = min((gcommand.x for gcommand in gcommands))
    xmax = max((gcommand.x for gcommand in gcommands))
    ymin = min((gcommand.y for gcommand in gcommands))
    ymax = max((gcommand.y for gcommand in gcommands))
    zmin = min((gcommand.z for gcommand in gcommands))
    zmax = max((gcommand.z for gcommand in gcommands))

    if label_layers:
        layer_names = [str(i + 1) for i in range(len())] if layer_names is None else layer_names

        float_distance = (ymax - ymin) / 10
        for layer_index, layer_name in enumerate(layer_names):
            ax.text(xmin, ymax + float_distance, layer_index * z_unit, layer_name, \
                    zdir=(-1, 0, 0))

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_xlim3d(xmin, xmax)
    ax.set_ylim3d(ymin, ymax)
    ax.set_zlim3d(zmin, zmax)

    if title is not None:
        plt.title(title)
    
    plt.legend()
    plt.show()

def flip_images(images):
    """
    Flip images vertically without overwriting

    images, list of height x width x 3 (color channels)

    return flipped_images, images where each image is flipped vertically
    """
    new_images = []

    for image in images:
        new_image = np.copy(image)
        for y in range(image.shape[0]):
            flipped_y = image.shape[0] - y - 1
            for x in range(image.shape[1]):
                pixel = image[y, x]
                new_image[flipped_y, x] = pixel
        new_images.append(new_image)

    return new_images

def main():
    """
    Printing demo
    """
    data = load_json("config.json")
    raws, layer_names = load_raw_images(data["folder"])
    flipped_images = flip_images(raws)

    gcommand_layers = convert_to_gcode(flipped_images, \
                                    usecs=data["usecs"], grid_unit=data["unitsize"], \
                                    z_unit=1.0, start_x=data["x"], start_y=data["y"])
    
    write_gcode(gcommand_layers, 'test.gcode', layer_names=layer_names, heatbed_temp=data["heatbed_temp"])
    graph(gcommand_layers, label_layers=True, grid_unit=data["unitsize"], z_unit=1.0, \
            start_x=data["x"], start_y=data["y"], layer_names=layer_names)

if __name__ == '__main__':
    main()
