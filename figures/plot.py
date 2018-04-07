import numpy as np
import matplotlib.pylab as plt
import pandas as pd
import seaborn as sns
sns.set(style="whitegrid", palette="muted")

fontsize = 24
fig_width_pt = 700.0
inches_per_pt = 1.0 / 72.27               # Convert pt to inch
golden_mean = (np.sqrt(5) - 1.0) / 2.0      # Aesthetic ratio
fig_width = fig_width_pt * inches_per_pt  # width in inches
fig_height = fig_width * golden_mean      # height in inches
fig_size = [fig_width, fig_height]
params = {'backend': 'ps',
          'font.family': 'serif',
          'font.serif':  'cm',
          'font.sans-serif': 'arial',
          'axes.labelsize': fontsize,
          'font.size': fontsize,
          'axes.titlesize': fontsize,
          'legend.fontsize': fontsize - 2,
          'xtick.labelsize': fontsize,
          'ytick.labelsize': fontsize,
          'text.usetex': True,
          'figure.figsize': fig_size,
          'lines.linewidth': 4}
plt.rcParams.update(params)


font_style = 'serif'
linewidth = 3
xscale = 'linear'
yscale = 'linear'
color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
color_ctr = 0

fig = plt.figure(figsize=(fig_width, fig_height))
plt.gcf()
ax = plt.gca()


def clear():
    font_style = 'serif'
    linewidth = 3
    xscale = 'linear'
    yscale = 'linear'
    plt.clf()
    color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    color_ctr = 0

    fontsize = 24
    fig_width_pt = 700.0
    inches_per_pt = 1.0 / 72.27               # Convert pt to inch
    golden_mean = (np.sqrt(5) - 1.0) / 2.0      # Aesthetic ratio
    fig_width = fig_width_pt * inches_per_pt  # width in inches
    fig_height = fig_width * golden_mean      # height in inches
    fig_size = [fig_width, fig_height]
    params = {'backend': 'ps',
              'font.family': 'serif',
              'font.serif':  'cm',
              'font.sans-serif': 'arial',
              'axes.labelsize': fontsize,
              'font.size': fontsize,
              'axes.titlesize': fontsize,
              'legend.fontsize': fontsize - 2,
              'xtick.labelsize': fontsize,
              'ytick.labelsize': fontsize,
              'text.usetex': True,
              'figure.figsize': fig_size,
              'lines.linewidth': 4}
    plt.rcParams.update(params)

    fig = plt.figure(figsize=(fig_width, fig_height))
    plt.gcf()


def set_scale(xscale, yscale):
    ax = plt.gca()
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    ax.set_autoscaley_on(False)


def set_figure_size(dim_inches):
    fig.set_size_inches(dim_inches)


def set_figure_dpi(dpi):
    fig.set_dpi(dpi)


def add_anchored_legend(ncol=2,
                        loc="upper center",
                        anchor=(0., 1.10, 1., .102),
                        frameon=False,
                        fontsize=22,
                        handles=None,
                        labels=None):
    if handles is None or labels is None:
        plt.legend(loc=loc, ncol=ncol, bbox_to_anchor=anchor,
                   frameon=frameon, fontsize=fontsize)
    else:
        plt.legend(loc=loc, ncol=ncol, bbox_to_anchor=anchor,
                   frameon=frameon, fontsize=fontsize, handles=handles,
                   labels=labels)


def add_legend(ncol=1,
               loc='best',
               frameon=False,
               fontsize=20,
               handles=None,
               labels=None):
    if handles is None or labels is None:
        plt.legend(loc=loc, ncol=ncol, frameon=frameon, fontsize=fontsize)
    else:
        plt.legend(loc=loc, ncol=ncol, frameon=frameon,
                   fontsize=fontsize, handles=handles, labels=lables)


def add_luke_options(legend_anchor=False):
    from matplotlib import rc
    font = {'family': 'serif',
            'size': 22}
    rc("font", **font)
    rc("lines", linewidth=3)

    ax = plt.gca()

    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # ax.xaxis.set_ticks_position('bottom')
    # ax.yaxis.set_ticks_position('left')
    plt.grid(True)
    ax.xaxis.grid(False)
    sns.despine(left=True, right=True)


def add_title(title):
    plt.title(title)


def add_labels(xlabel, ylabel):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def set_xlim(xmin=None, xmax=None):
    ax = plt.gca()
    if xmin is None:
        xmin, _ = ax.get_xlim()
    if xmax is None:
        _, x1 = ax.get_xlim()
        xmax = x1 + (x1 / 20.0)
    ax.set_xlim((xmin, xmax))


def set_ylim(ymin=None, ymax=None):
    ax = plt.gca()

    ax.set_autoscaley_on(False)
    if ymin is None:
        y0, _ = ax.get_ylim()
        ymin = y0 - (y0 / 50.0)
    if ymax is None:
        _, ymax = ax.get_ylim()
    ax.set_ylim(ymin, ymax)
    ax.axis('tight')


def set_xticklabels(xticklabels,
                    rotation='vertical',
                    fontsize=16):
    ax = plt.gca()
    ax.set_xticklabels(xticklabels, rotation=rotation,
                       fontsize=fontsize)


def set_xticks(xdata, xticklabels, rotation='horizontal'):
    ax = plt.gca()
    ax.set_xticks(xdata)
    ax.set_xticklabels(xticklabels, rotation=rotation)


def set_yticklabels(yticklabels,
                    rotation='horizontal',
                    fontsize=16):
    ax = plt.gca()
    ax.set_yticklabels(yticklabels, rotation=rotation,
                       fontsize=fontsize)


def set_yticks(ydata, yticklabels, rotation='horizontal'):
    ax = plt.gca()
    ax.set_yticks(ydata)
    ax.set_yticklabels(yticklabels, rotation=rotation)


def line_plot(y_data, x_data=None, label=None, tickmark='-', color=None,
              markevery=1, alpha=1.0, markersize=3, ax=plt):
    global color_ctr
    if x_data is None:
        x_data = np.arange(0, len(y_data))
    if color is None:
        color = color_list[color_ctr]
        color_ctr = (color_ctr + 1) % len(color_list)

    return ax.plot(x_data, y_data, tickmark, label=label,
                   color=color, markevery=markevery, clip_on=False,
                   alpha=alpha, linewidth=markersize)


def scatter_plot(x_data, y_data, color=None, tickmark='o', **kargs):
    global color_ctr
    if color == None:
        color = color_list[color_ctr]
        color_ctr = (color_ctr + 1) % len(color_list)

    return plt.scatter(x_data, y_data, c=color, edgecolors='none', clip_on=False, marker=tickmark, **kargs)


def barplot(x_data, y_data, groups=None, stack=False, ax=None, color_name=None):
    if ax is None:
        ax = plt.gca()
    bplot = ""
    if groups is None:
        colors = sns.color_palette(n_colors=1)
        bplot = sns.barplot(x=x_data, y=y_data, color=colors[0], ax=ax)
    else:
        if stack:
            colors = sns.color_palette(n_colors=len(groups))
            plots = list()
            for i in range(len(groups)):
                pd_dict = dict()
                pd_dict['x'] = x_data
                pd_dict[groups[i]] = y_data[i]
                df = pd.DataFrame(pd_dict)
                df = df.melt(id_vars=['x'], var_name='measure',
                             value_vars=[groups[i]],
                             value_name='time')
                bplot = sns.barplot(ax=ax, data=df, x='x',
                                    y='time', color=colors[i])
        else:
            pd_dict = dict()
            pd_dict['x'] = x_data
            for i in range(len(groups)):
                pd_dict[groups[i]] = y_data[i]
            df = pd.DataFrame(pd_dict)
            df = df.melt(id_vars=['x'], var_name='measure', value_vars=groups,
                         value_name='time')
            bplot = sns.barplot(data=df, x='x', y='time',
                                hue='measure', ax=ax, palette=color_name)

        import matplotlib.patches as patches
        objs = ax.findobj(match=patches.Rectangle)
        legend_lines = list()
        ctr = 0
        for i in range(len(groups)):
            legend_lines.append(objs[ctr])
            ctr += len(x_data)
        n_cols = ((len(groups) - 1) / 2) + 1
        if (n_cols < 2):
            n_cols = 2
        add_anchored_legend(handles=legend_lines, labels=groups, ncol=n_cols)
    return bplot


def bar_plot(**kwargs):
    return sns.barplot(**kwargs)


def violin_plot(x_data, y_data, groups, split):
    return sns.violinplot(x=x_data, y=y_data, hue=groups, split=split)


def spy(A, color='blue', markersize=1, markeredgewidth=0.0):
    return plt.spy(A, color=color, markersize=markersize,
                   markeredgewidth=markeredgewidth)


def save_plot(filename, clear_plot=True):
    plt.savefig(filename, bbox_inches="tight", clip_on=False,
                transparent=True)
    if clear_plot:
        clear()


def display_plot():
    plt.show()
