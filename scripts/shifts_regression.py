import pandas as pd
import scipy.stats
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rc

rc('text', usetex = True)

plt.xlabel('time')
plt.ylabel('shift among pairs')

fig_size = 6
pos = 1

shifts = pd.read_csv('output/shifts.csv')
for pair, values in shifts.groupby(['filename_1', 'filename_2']):
    starts = values['start'].tolist()
    shifts = values['shift'].tolist()
    n = values['start'].shape[0]

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(
        starts,
        shifts
    )
    print(slope*86400, p_value, std_err)

    fit_y = [slope * x + intercept for x in starts]

    residuals = sum([
        (y - yf)**2
        for y, yf in zip(shifts, fit_y)
    ])

    rms = np.sqrt(residuals/n)

    if pos <= fig_size**2:
        plt.subplot(fig_size, fig_size, pos)
        plt.scatter(x = starts, y = shifts, s = 1)
        plt.plot(starts, fit_y, linewidth = 0.5)
        plt.xlim(0, 86400)
        plt.xticks([])
        plt.yticks([])
        if not np.isnan(p_value):
            plt.xlabel("rms = {:.3f}".format(rms), size = 6)

        pos += 1

plt.savefig("reports/shifts.pdf")
plt.show()
