#! env python

import sys
import pandas as pd
import matplotlib.pylab as plt
import yaml
import os.path as path

def key_exists(element, *keys):
    if type(element) is not dict:
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True

if len(sys.argv) < 3:
    sys.exit(1)

csv_path = sys.argv[1]
out_path = sys.argv[2]




## Look for a yaml file in the same dir as the csv file
yaml_file = path.join(path.dirname(csv_path), "plot.yml")

if path.exists(yaml_file):
    with open(yaml_file, 'rb') as f:
        cfg = yaml.load(f)
        print cfg

data = pd.read_csv(csv_path, index_col=0)

ax = data.plot(kind='line')

if key_exists(cfg, "xaxis", "scale"):
    ax.set_xscale(cfg["xaxis"]["scale"], nonposx='clip')

if key_exists(cfg, "yaxis", "label"):
    ax.set_ylabel(cfg["yaxis"]["label"])

# plt.show()

plt.savefig(sys.argv[2], bbox_inches="tight", clip_on=False, transparent=True)
