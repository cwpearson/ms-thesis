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


def col_to_idx(s):
    if isinstance(s, int):
        return s

    acc = 0
    for place in range(len(s)):
        c = s[place - len(s)]
        if place == len(s) - 1:
            int_val = ord(c.lower()) - 98
        else:
            int_val = ord(c.lower()) - 97

        acc += int_val + (26 ** place)
    return acc


if len(sys.argv) < 2:
    sys.exit(1)

yaml_path = sys.argv[1]

yaml_dir = path.dirname(yaml_path)



with open(yaml_path, 'rb') as f:
    cfg = yaml.load(f)
    print cfg

for plot_path, plot_cfg in cfg.iteritems():
    if not path.isabs(plot_path):
        plot_path = path.join(yaml_dir, plot_path)
    print plot_path, plot_cfg

    # build data frame from specified columns
    data = pd.DataFrame()
    for s in plot_cfg["series"]:
        file_path = s["file"]
        if not path.isabs(file_path):
            file_path = path.join(yaml_dir, file_path)
        print "reading", file_path
        csv = pd.read_csv(file_path)
        col_idx = col_to_idx(s["col"])
        print "selecting column", col_idx
        col = csv.iloc[:, col_idx]
        if "label" in s:
            label = s["label"]
            print "renaming to", label
        else:
            label = col.name
        data.loc[:, label] = col
    # set column 0 as index 
    data = data.set_index(data.iloc[:, 0].name, drop=True)
    #print data

    # Generate and configure plot
    ax = data.plot(kind='line')

    if "yaxis" in plot_cfg:
        axis_cfg = plot_cfg["yaxis"]
        if axis_cfg and "lim" in axis_cfg:
            lim = axis_cfg["lim"]
            print "setting ylim", lim
            ax.set_ylim(lim)
        if axis_cfg and "label" in axis_cfg:
            label = axis_cfg["label"]
            print "setting ylabel", label
            ax.set_ylabel(label)

    if "xaxis" in plot_cfg:
        axis_cfg = plot_cfg["xaxis"]
        if axis_cfg and "scale" in axis_cfg:
            scale = axis_cfg["scale"]
            print "setting xscale", scale
            ax.set_xscale(scale)
        if axis_cfg and "label" in axis_cfg:
            label = axis_cfg["label"]
            print "setting xlabel", label
            ax.set_xlabel(label)

    if "title" in plot_cfg:
        title = plot_cfg["title"]
        print "setting title", title
        ax.set_title(title)

    # Save plot
    print "saving to", plot_path
    plt.savefig(plot_path, bbox_inches="tight", clip_on=False, transparent=True)
