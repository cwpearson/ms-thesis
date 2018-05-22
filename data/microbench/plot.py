#! /usr/bin/env python3

import json
import sys
import pprint
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import yaml

pp = pprint.PrettyPrinter(indent=4)

def generator_old(fig, yaml_dir, plot_cfg):
    ax = fig.add_subplot(111)
    # build data frame from specified entries
    for s in plot_cfg["series"]:
        file_path = s["file"]
        label = s["label"]
        if "regex" in s:
            regex = s["regex"]
        else:
            regex = ".*"
        print("Using regex:", regex)
        if not os.path.isabs(file_path):
            file_path = os.path.join(yaml_dir, file_path)
        print("reading", file_path)
        with open(file_path, "rb") as f:
            j = json.loads(f.read().decode('utf-8'))
        
        pattern = re.compile(regex)
        matches = [b for b in j["benchmarks"] if pattern == None or pattern.search(b["name"])]
        means = [b for b in matches if b["name"].endswith("_mean")]
        stddevs = [b for b in matches if b["name"].endswith("_stddev")]
        x = np.array([int(b["bytes"]) for b in means])
        y = np.array([float(b["bytes_per_second"]) for b in means])
        e = np.array([float(b["bytes_per_second"]) for b in stddevs])

        # pp.pprint(means)

        ax.errorbar(x, y, e, capsize=3, label=label)

    if "yaxis" in plot_cfg:
        axis_cfg = plot_cfg["yaxis"]
        if axis_cfg and "lim" in axis_cfg:
            lim = axis_cfg["lim"]
            print("setting ylim", lim)
            ax.set_ylim(lim)
        if axis_cfg and "label" in axis_cfg:
            label = axis_cfg["label"]
            print("setting ylabel", label)
            ax.set_ylabel(label)

    if "xaxis" in plot_cfg:
        axis_cfg = plot_cfg["xaxis"]
        if axis_cfg and "scale" in axis_cfg:
            scale = axis_cfg["scale"]
            print("setting xscale", scale)
            ax.set_xscale(scale, basex=2)
        if axis_cfg and "label" in axis_cfg:
            label = axis_cfg["label"]
            print("setting xlabel", label)
            ax.set_xlabel(label)

    if "title" in plot_cfg:
        title = plot_cfg["title"]
        print("setting title", title)
        ax.set_title(title)

    ax.legend()

    return fig


def generate_figure(plot_cfg, root_dir):

    fig = plt.figure()

    if "generator" in plot_cfg:
        if plot_cfg["generator"] == "df":
            fig = generator_df(fig, root_dir, plot_cfg)
        elif plot_cfg["generator"] == "regplot":
            fig = generator_regplot(fig, root_dir, plot_cfg)
        else:
            print("Unhandled generator!")
            assert False
    else:
        fig = generator_old(fig, root_dir, plot_cfg)

    return fig

if __name__ == '__main__':

    if len(sys.argv) == 3:
        output_path = sys.argv[1]
        yaml_path = sys.argv[2]
    else:
        sys.exit(1)

    root_dir = os.path.dirname(os.path.abspath(yaml_path))

    # load the config
    with open(yaml_path, 'rb') as f:
        cfg = yaml.load(f)

    fig = generate_figure(cfg, root_dir)

    # Save plot
    print("saving to", output_path)
    fig.savefig(output_path, bbox_inches="tight",
                clip_on=False, transparent=True)