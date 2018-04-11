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
        print "selecting column", s["col"]
        col = csv.iloc[:, s["col"]]
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
        if "lim" in axis_cfg:
            lim = axis_cfg["lim"]
            print "setting ylim", lim
            ax.set_ylim(lim)
        if "label" in axis_cfg:
            label = axis_cfg["label"]
            print "setting ylabel", label
            ax.set_ylabel(label)

    if "xaxis" in plot_cfg:
        axis_cfg = plot_cfg["xaxis"]
        if "scale" in axis_cfg:
            scale = axis_cfg["scale"]
            print "setting xscale", scale
            ax.set_xscale(scale)
        if "label" in axis_cfg:
            label = axis_cfg["label"]
            print "setting xlabel", label
            ax.set_xlabel(label)

    # Save plot
    print "saving to", plot_path
    plt.savefig(plot_path, bbox_inches="tight", clip_on=False, transparent=True)


# def cfg_exists(*keys):
#     if key_exists(cfg, *("plots", csv_name,) + keys):
#         return True
#     if key_exists(cfg, *("plots", "default",) + keys):
#         return True
#     return False   

# def cfg_get(*keys):
#     if key_exists(cfg, *("plots", csv_name,) + keys):
#         return get(cfg, *("plots", csv_name,) + keys)
#     return get(cfg, *("plots", "default") + keys)

# data = pd.read_csv(csv_path, index_col=0)
# ax = data.plot(kind='line')


# if cfg_exists("xaxis", "scale"):
#     print out_path, ": setting custom xaxis scale"
#     ax.set_xscale(cfg_get("xaxis", "scale"), nonposx='clip')

# if cfg_exists("yaxis", "label"):
#     print out_path, ": setting custom yaxis label"
#     ax.set_ylabel(cfg_get("yaxis","label"))

# if cfg_exists("yaxis", "lim"):
#     print out_path, ": setting custom ylim"
#     lim = cfg_get("yaxis", "lim")
#     ax.set_ylim(lim)

# if cfg_exists("title"):
#     print out_path, ": setting custom title"
#     plt.title(cfg_get("title"))

# if cfg_exists("series"):
#     for series in cfg_get("series"):
#         if cfg_exists("series", series, "color"):
#             print out_path, ": setting custom color"
#             plt.gca().get_lines()[series].set_color(cfg_get("series", series, "color"))
#         if cfg_exists("series", series, "style"):
#             print out_path, ": setting custom style"
#             plt.gca().get_lines()[series].set_linestyle(cfg_get("series", series, "style"))
#         if cfg_exists("series", series, "lw"):
#             print out_path, ": setting custom lw"
#             plt.gca().get_lines()[series].set_lw(cfg_get("series", series, "lw"))
#         ax.legend() # regenerate legend

# # Set labels last
# h, l = ax.get_legend_handles_labels()
# if cfg_exists("series"):
#     for series in cfg_get("series"):
#         if cfg_exists("series", series, "label"):
#             print out_path, ": setting custom label"
#             l[series]=cfg_get("series", series, "label")
# ax.legend(h, l)


# # plt.show()
# plt.savefig(sys.argv[2], bbox_inches="tight", clip_on=False, transparent=True)
