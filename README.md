# Sod shock tube calculator

A simple package to numerically solve the sod shock tube problem for python 2.7 and 3.5+, including a modified solution
for a dust-gas mixture as used in the 3D hydrodymamic simulations presented in my PhD Thesis, [Backus(2017)](http://hdl.handle.net/1773/40959).

This repository is a fork of the Riemann solver implemented at [https://gitlab.com/fantaz/Riemann_exact](https://gitlab.com/fantaz/Riemann_exact), which is itself just a pythonic clone of the [fortran code by Bruce Fryxell](http://cococubed.asu.edu/codes/riemann/exact_riemann.f).

## Installation

### Install from PYPI

```
pip install sodshock
```

### Install from source
* Clone the repository: `git clone https://github.com/ibackus/sod-shocktube.git`
* cd into the directory: `cd sod-shocktube`
* and install with pip: ```pip install .``` Or else `python setup.py install`


## Description
The Sod shock tube is a Riemann problem used as a standard test problem in computational hydrodynamics.
Checkout the article in [Wikipedia](http://en.wikipedia.org/wiki/Sod_shock_tube)
for a more complete description of the Sod problem.
This module should calculate analytical solutions for various initial conditions.
To see it in action, check out rendered ipython notebook example 
[here](http://nbviewer.ipython.org/urls/gitlab.com/fantaz/Riemann_exact/raw/master/sod.ipynb).

### Standard test case
In the standard case the density and pressure on the left are unity,
and the density on the right side of the contact is 0.125 and the pressure is 0.1.
The ratio of specific heats is 1.4.


## About the code
The code logic is blatantly copied from dr. Timmes' [website](http://cococubed.asu.edu/code_pages/exact_riemann.shtml).
Sod solver returns after time of evolution the following variables:
1. Positions of head and foot of rarefation wave, contact discontinuity and shock
2. Constant pressure, density and velocity for all regions except rarefaction region
3. Pressure, density and velocity sampled across the domain of interest

The usage should be straightforward (see `examples/exactRiemann.py`:

---

```python

import sodshock
import matplotlib.pyplot as plt


if __name__ == '__main__':

    gamma = 1.4
    dustFrac = 0.0
    npts = 500
    t = 0.2
    left_state = (1,1,0)
    right_state = (0.1, 0.125, 0.)

    # left_state and right_state set pressure, density and u (velocity)
    # geometry sets left boundary on 0., right boundary on 1 and initial
    # position of the shock xi on 0.5
    # t is the time evolution for which positions and states in tube should be 
    # calculated
    # gamma denotes specific heat
    # note that gamma and npts are default parameters (1.4 and 500) in solve 
    # function
    positions, regions, values = sodshock.solve(left_state=left_state, \
        right_state=right_state, geometry=(0., 1., 0.5), t=t, 
        gamma=gamma, npts=npts, dustFrac=dustFrac)
    # Printing positions
    print('Positions:')
    for desc, vals in positions.items():
        print('{0:10} : {1}'.format(desc, vals))

    # Printing p, rho and u for regions
    print('Regions:')
    for region, vals in sorted(regions.items()):
        print('{0:10} : {1}'.format(region, vals))

    # Finally, let's plot the solutions
    f, axarr = plt.subplots(len(values)-1, sharex=True)

    axarr[0].plot(values['x'], values['p'], linewidth=1.5, color='b')
    axarr[0].set_ylabel('pressure')
    axarr[0].set_ylim(0, 1.1)

    axarr[1].plot(values['x'], values['rho'], linewidth=1.5, color='r')
    axarr[1].set_ylabel('density')
    axarr[1].set_ylim(0, 1.1)

    axarr[2].plot(values['x'], values['u'], linewidth=1.5, color='g')
    axarr[2].set_ylabel('velocity')
    
    plt.suptitle('Shocktube results at t={0}\ndust fraction = {1}, gamma={2}'\
                 .format(t, dustFrac, gamma))
    plt.show()

```

---

Which should give us the following output:
```
Positions:
Shock      : 0.8504311464060357
Contact Discontinuity : 0.6854905240097902
Head of Rarefaction : 0.26335680867601535
Foot of Rarefaction : 0.4859454374877634
Regions:
Region 1   : (1, 1, 0)
Region 2   : RAREFACTION
Region 3   : (0.30313017805064707, 0.42631942817849544, 0.92745262004895057)
Region 4   : (0.30313017805064707, 0.26557371170530725, 0.92745262004895057)
Region 5   : (0.1, 0.125, 0.0)
```
Let's not forget the plots:

![pressure](https://github.com/ibackus/sod-shocktube/blob/master/figs/pressure.png)
![density](https://github.com/ibackus/sod-shocktube/blob/master/figs/density.png)
![velocity](https://github.com/ibackus/sod-shocktube/blob/master/figs/velocity.png)
![energy](https://github.com/ibackus/sod-shocktube/blob/master/figs/energy.png)
![temperature](https://github.com/ibackus/sod-shocktube/blob/master/figs/temperature.png)

---

## Licence

The MIT License (MIT)

Copyright (c) 2015 Jerko Škifić

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
