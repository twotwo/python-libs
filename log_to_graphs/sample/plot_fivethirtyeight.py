"""
This shows an example of the "fivethirtyeight" styling, which
tries to replicate the styles from FiveThirtyEight.com.

http://matplotlib.org/examples/style_sheets/plot_fivethirtyeight.html
"""


from matplotlib import pyplot as plt
import numpy as np

N = 24
x = np.arange(N)
y = np.linspace(0, 100, N)
value = np.linspace(1000, 5000, N)

def autolabel(bars, axes):
	# attach some text labels
	for bar in bars:
		height = bar.get_height()
		axes.text(bar.get_x() + bar.get_width()/2., 1.05*height,
				'%d' % int(height),
				ha='center', va='bottom')

def text(axes, xs, y, values):
	for x, value in zip(xs, values):
		axes.text(x, y, '%d' % int(value), fontsize=4, bbox=dict(facecolor='red', alpha=0.2),
			ha='center', va='bottom')

with plt.style.context('fivethirtyeight'):
	# plt.plot(x, np.sin(x) + x + np.random.randn(N))
	# plt.plot(x, np.sin(x) + 0.5 * x + np.random.randn(N))
	# plt.plot(x, np.sin(x) + 2 * x + np.random.randn(N))
	# plt.plot(x, np.sin(x) + 4 * x + np.random.randn(N))
	# plt.plot(x, 1.5 * x)
	fig, axes = plt.subplots(figsize=(18, 10))
	axes.plot(x, np.sin(y) + y + np.random.randn(N))
	bars1 = axes.bar(x, y, width=0.35, yerr=np.sin(x))
	bars2 = axes.bar(x+0.35, 1.2* y+np.random.randn(N), width=0.35, yerr=np.sin(x))
	# plt.text(x, np.linspace(-5, -5, N), value, bbox=dict(facecolor='red', alpha=0.5))
	text(axes, x+0.5, -10, value)
	autolabel(bars1, axes)
	autolabel(bars2, axes)

plt.show()
