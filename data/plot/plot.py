#! env python

import sys
import pandas as pd
import matplotlib.pylab as plt
import yaml
import os.path as path
import pprint

pp = pprint.PrettyPrinter(indent=4)

def key_exists(element, *keys):
    if type(element) is not dict:
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError as e:
            return False
    return True

def get(element, *keys):
    _element = element
    for key in keys:
        _element = _element[key]
    return _element






if len(sys.argv) < 3:
    sys.exit(1)

csv_path = sys.argv[1]
out_path = sys.argv[2]

csv_name = path.basename(csv_path)



## Look for a yaml file in the same dir as the csv file
yaml_file = path.join(path.dirname(csv_path), "plots.yml")

cfg = {}
if path.exists(yaml_file):
    with open(yaml_file, 'rb') as f:
        cfg = yaml.load(f)
# pp.pprint(cfg)

def cfg_exists(*keys):
    if key_exists(cfg, *("plots", csv_name,) + keys):
        return True
    if key_exists(cfg, *("plots", "default",) + keys):
        return True
    return False   

def cfg_get(*keys):
    if key_exists(cfg, *("plots", csv_name,) + keys):
        return get(cfg, *("plots", csv_name,) + keys)
    return get(cfg, *("plots", "default") + keys)

data = pd.read_csv(csv_path, index_col=0)
ax = data.plot(kind='line')


if cfg_exists("xaxis", "scale"):
    print out_path, ": setting custom xaxis scale"
    ax.set_xscale(cfg_get("xaxis", "scale"), nonposx='clip')

if cfg_exists("yaxis", "label"):
    print out_path, ": setting custom yaxis label"
    ax.set_ylabel(cfg_get("yaxis","label"))

if cfg_exists("title"):
    print out_path, ": setting custom title"
    plt.title(cfg_get("title"))

if cfg_exists("series"):
    for series in cfg_get("series"):
        if cfg_exists("series", series, "color"):
            print out_path, ": setting custom color"
            plt.gca().get_lines()[series].set_color(cfg_get("series", series, "color"))
        if cfg_exists("series", series, "style"):
            print out_path, ": setting custom style"
            plt.gca().get_lines()[series].set_linestyle(cfg_get("series", series, "style"))
        if cfg_exists("series", series, "lw"):
            print out_path, ": setting custom lw"
            plt.gca().get_lines()[series].set_lw(cfg_get("series", series, "lw"))
        ax.legend() # regenerate legend

# Set labels last
h, l = ax.get_legend_handles_labels()
if cfg_exists("series"):
    for series in cfg_get("series"):
        if cfg_exists("series", series, "label"):
            print out_path, ": setting custom label"
            l[series]=cfg_get("series", series, "label")
ax.legend(h, l)


# plt.show()
plt.savefig(sys.argv[2], bbox_inches="tight", clip_on=False, transparent=True)
