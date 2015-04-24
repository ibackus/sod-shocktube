# Sod shock tube calculator

## Description
The Sod shock tube is a Riemann problem used as a standard test problem in computational hydrodynamics. 
Checkout the article in [Wikipedia](http://en.wikipedia.org/wiki/Sod_shock_tube)
for a more complete description of the Sod problem.
This module should calculate analytical solutions for various initial conditions.

### Standard test case
In the standard case the density and pressure on the left are unity, 
and the density on the right side of the contact is 0.125 and the pressure is 0.1. 
The ratio of specific heats is 1.4. 


## About the code
The code logic is blatantly copied from dr. Timmes' [website](http://cococubed.asu.edu/code_pages/exact_riemann.shtml).
Usage should be straightforward:
```python
import sod
def fun():
    positions, regions, values = sod.solve(left_state=(1, 1, 0), right_state=(0.1, 0.125, 0.),
                                           geometry=(0., 1., 0.5), t=0.2, gamma=1.4, npts=500)
```
Sod solver returns after time of evolution the following variables:
1. Positions of head and foot of rarefation wave, contact discontinuity and shock
2. Constant pressure, density and velocity for all regions except rarefaction region
3. Pressure, density and velocity sampled across the domain of interest

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