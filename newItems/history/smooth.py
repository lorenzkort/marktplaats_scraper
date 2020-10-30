import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

x = np.linspace(0, 10, num=20, endpoint=True)
y = np.cos(-x**2/9.0)
f = interp1d(x, y, kind='quadratic')

xnew = np.linspace(0, 10, num=1000, endpoint=True)
plt.plot(x, y, 'o')
plt.plot(xnew, f(xnew))
plt.show()