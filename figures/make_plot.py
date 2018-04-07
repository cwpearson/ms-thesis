#! env python

import sys
import pandas as pd
import matplotlib.pylab as plt

if len(sys.argv) < 3:
    sys.exit(1)

csv_path = sys.argv[1]

data = pd.read_csv(csv_path, index_col=0)

ax = data.plot(kind='line')

ax.set_xscale("log", nonposx='clip')

# plt.show()

plt.savefig(sys.argv[2], bbox_inches="tight", clip_on=False, transparent=True)
