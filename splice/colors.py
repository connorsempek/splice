# flat ui color scheme

# imports
import os
import json
import random

# TO DO: Turn json file into list of dicts of the form, e.g., 
# {'name': 'Aqua Island', 'hex': '#A2DED0', 'rgba': 'rgba(162, 222, 208, 1)'}
def get_color_blob():

    fn = 'flat_ui_colors.json'
    fp = os.path.join(os.path.dirname(os.path.realpath(__file__)), fn)
    with open(fp, 'r') as f:
        color_blob = json.load(f)
    return color_blob


def make_hex_color_map(slices, seed=None):
    
    
    blob = get_color_blob()
    hexes = [d['hex'] for d in blob['all'].values()]
    
    if not slices:
        res = hexes[0]
    else:
        random.seed(seed)
        idx = random.sample(range(len(slices)), len(slices))
        res = {slc: hexes[idx[i]] for i, slc in enumerate(slices)}
    return res


def make_rgba_color_map(slices, seed=None):
    

    blob = get_color_blob()
    rgbas = [d['rgba'] for d in blob['all'].values()]
    
    if not slices:
        res = rgbas[0]
    else:
        random.seed(seed)
        idx = random.sample(range(len(slices)), len(slices))
        res = {slc: rgbas[idx[i]] for i, slc in enumerate(slices)}
    return res