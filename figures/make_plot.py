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
pp.pprint(cfg)

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
    print "setting custom xaxis scale"
    ax.set_xscale(cfg_get("xaxis", "scale"), nonposx='clip')

if cfg_exists("yaxis", "label"):
    print "setting custom yaxis label"
    ax.set_ylabel(cfg_get("yaxis","label"))

if cfg_exists("title"):
    print "setting custom title"
    plt.title(cfg_get("title"))


# plt.show()

plt.savefig(sys.argv[2], bbox_inches="tight", clip_on=False, transparent=True)
