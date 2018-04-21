#! /usr/bin/env python

import sys
import pandas as pd
import matplotlib.pylab as plt
import yaml
import os.path as path
import pprint
import seaborn as sns
import scipy

pp = pprint.PrettyPrinter(indent=4)


def key_exists(element, *keys):
    if type(element) is not dict:
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError(
            'keys_exists() expects at least two arguments, one given.')

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
    elif not isinstance(s, str):
        raise TypeError

    acc = 0
    for idx in range(len(s)):
        place = len(s) - 1 - idx
        c = s[idx]
        if place == 1:
            int_val = ord(c.lower()) - 96
        else:
            int_val = ord(c.lower()) - 97

        acc += int_val * (26 ** place)
    return acc


def generator_old(fig, yaml_dir, plot_cfg):
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
    # print data

    ax = fig.add_subplot(111)

    # Generate and configure plot
    ax = data.plot(kind='line', ax=ax)

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

    return fig


def handle_keep(df, colStr, valStr, opStr):
    if not opStr:
        opStr = "="

    if opStr == "=":
        df = df.loc[df[colStr] == valStr]
    elif opStr == "gt":
        df = df.loc[df[colStr] > valStr]
    else:
        print "opStr was", opStr
        assert False

    return df


def generator_df(fig, yaml_dir, plot_cfg):

    file_path = plot_cfg["file"]
    if not path.isabs(file_path):
        file_path = path.join(yaml_dir, file_path)

    df = pd.read_csv(file_path)

    groups = plot_cfg["reduce-over"]
    print "reducing by", groups
    means = df.groupby(groups).mean()
    maxes = df.groupby(groups).max()
    errors = df.groupby(groups).std()

    means = means.rename(columns={"bandwidth": "bandwidth (mean)"})
    maxes = maxes.rename(columns={"bandwidth": "bandwidth (max)"})
    errors = errors.rename(columns={"bandwidth": "bandwidth (std)"})

    df = pd.concat([maxes, errors], axis=1)
    df = df.reset_index()

    print df

    for keep in plot_cfg["keep"]:
        colStr = keep["col"]
        valStr = keep["val"]
        opStr = keep["op"]
        df = handle_keep(df, colStr, valStr, opStr)

    ax = fig.add_subplot(111)

    for key, grp in df.groupby(["threads"]):
        max_per_threads = grp.groupby("transfer_size").max()
        max_per_threads.plot(ax=ax, y="bandwidth (max)",
                             linestyle="--", label=str(key) + " threads")

    # Find max overall bandwidth by transfer_size
    by_count = df.groupby(["transfer_size"])
    max_bw = by_count.max()

    print max_bw

    ax = max_bw.plot(ax=ax, kind="line", y="bandwidth (max)",
                     label="max observed")

    ax.set_xscale("log")
    ax.set_ylim(bottom=0)
    plt.legend()

    return fig


def generator_regplot(fig, yaml_dir, plot_cfg):
    file_path = plot_cfg["file"]
    if not path.isabs(file_path):
        file_path = path.join(yaml_dir, file_path)

    df = pd.read_csv(file_path)

    xdata_cfg = plot_cfg.get("xdata", {})
    x_col_idx = col_to_idx(xdata_cfg.get("col", 0))
    x_col = df.iloc[:, x_col_idx]

    ax = fig.add_subplot(111)
    y_cfgs = plot_cfg.get("ydata", [])
    for y_cfg in y_cfgs:
        print y_cfg
        col_idx = col_to_idx(y_cfg["col"])
        col = df.iloc[:, col_idx]
        color = y_cfg.get("color", "black")

        label = y_cfg.get("label", col.name)

        ax = sns.regplot(ax=ax, x=x_col, y=col, data=df,
                         ci=68, label=label, color=color)

    # Set limits
    ax.set_ylim([0, 1600])
    ax.set_ylabel("Traversal Time (us)")

    # update labels
    h, l = ax.get_legend_handles_labels()
    for c, col in enumerate(y_cfgs):
        def get_linregress(series):
            return scipy.stats.linregress(x=ax.get_lines()[series].get_xdata(), y=ax.get_lines()[series].get_ydata())
        slope, intercept, r_value, p_value, std_err = get_linregress(c)
        l[c] = l[c] + ": " + str(slope) + " us/fault"
    ax.legend(h, l)

    return fig


def generate_figure(plot_cfg, root_dir):

    fig = plt.figure()

    if "generator" in plot_cfg:
        if plot_cfg["generator"] == "df":
            fig = generator_df(fig, root_dir, plot_cfg)
        elif plot_cfg["generator"] == "regplot":
            fig = generator_regplot(fig, root_dir, plot_cfg)
        else:
            print "Unhandled generator!"
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

    root_dir = path.dirname(yaml_path)

    # load the config
    with open(yaml_path, 'rb') as f:
        cfg = yaml.load(f)

    fig = generate_figure(cfg, root_dir)

    # Save plot
    print "saving to", output_path
    fig.savefig(output_path, bbox_inches="tight",
                clip_on=False, transparent=True)
