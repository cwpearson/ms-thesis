import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy
import sys
sns.set(style="whitegrid")


if len(sys.argv) < 3:
    sys.exit(1)

csv_path = sys.argv[1]
out_path = sys.argv[2]

# Load the example titanic dataset
df = pd.read_csv(csv_path)


x_col = df.iloc[:, 0]
y_cols = df.iloc[:, 1:]

# print x_col
# print ""

colors = ["black", "gray"]

## Draw plots
for c, col in enumerate(y_cols):
    ax = sns.regplot(x=x_col, y=col, data=df, ci=68, label="gpu0:cpu0 Traversal Time (us) [managed]", color=colors[c])

## Set limits
ax.set_ylim([0,1600])
ax.set_ylabel("Traversal Time (us)")


#update labels
h, l = ax.get_legend_handles_labels()
for c, col in enumerate(y_cols):
    def get_linregress(series):
        return scipy.stats.linregress(x=ax.get_lines()[series].get_xdata(),y=ax.get_lines()[series].get_ydata())
    slope, intercept, r_value, p_value, std_err = get_linregress(c)
    l[c] = col +": " + str(slope) + " us/fault"
ax.legend(h, l)

plt.savefig(out_path, bbox_inches="tight", clip_on=False, transparent=True)
# plt.show()