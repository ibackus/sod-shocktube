import math
import sys
import numpy as np


def f(p4, p1, p5, rho1, rho5, gamma):
    z = (p4 / p5 - 1.)
    c1 = math.sqrt(gamma * p1 / rho1)
    c5 = math.sqrt(gamma * p5 / rho5)

    gm1 = gamma - 1.
    gp1 = gamma + 1.
    g2 = 2. * gamma

    fact = gm1 / g2 * (c5 / c1) * z / math.sqrt (1. + gp1 / g2 * z)
    fact = (1. - fact) ** (g2 / gm1)

    return p1 * fact - p4


if __name__ == '__main__':
    # ..define initial conditions
    # ..state at left of discontinuity
    rhol = 1.0
    pl = 1.0
    ul = 0.

    # ..state at right of discontinuity
    rhor = 0.125
    pr = 0.1
    ur = 0.

    # .. equation of state
    gamma = 1.4

    # ..location of discontinuity at t = 0
    xi = 0.5

    # ..time at which solution is desired
    t = 0.20

    # ..number of points in solution
    npts = 500

    # ..spatial interval over which to compute solution
    xl = 0.0
    xr = 1.0

    # ..begin solution
    if pl > pr:
         rho1 = rhol
         p1   = pl
         u1   = ul
         rho5 = rhor
         p5   = pr
         u5   = ur
    else:
         rho1 = rhor
         p1   = pr
         u1   = ur
         rho5 = rhol
         p5   = pl
         u5   = ul

    # ..solve for post-shock pressure by secant method
    # ..initial guesses
    p40 = p1
    p41 = p5
    f0 = f(p40, p1, p5, rho1, rho5, gamma)

    # ..maximum number of iterations and maximum allowable relative error
    itmax = 20
    eps = 1.e-5

    err = 1.
    iter = 0
    itermax = 20
    while err > eps:
        f1 = f(p41, p1, p5, rho1, rho5, gamma)
        if math.fabs((f1-f0)/f1) < eps:
            break
        p4 = p41 - (p41 - p40) * f1 / (f1 - f0)
        error = math.fabs(p4 - p41) / p41
        if error < eps:
            break
        p40 = p41
        p41 = p4
        f0 = f1
        iter +=1
        if iter > itermax:
            print("no convergence!")
            sys.exit()

    # c..compute post-shock density and velocity
    z = (p4 / p5 - 1.)
    c5 = math.sqrt(gamma * p5 / rho5)

    gm1 = gamma - 1.
    gp1 = gamma + 1.
    gmfac1 = 0.5 * gm1 / gamma
    gmfac2 = 0.5 * gp1 / gamma

    fact = math.sqrt(1. + gmfac2 * z)

    u4 = c5 * z / (gamma * fact)
    rho4 = rho5 * (1. + gmfac2 * z) / (1. + gmfac1 * z)

    # c..shock speed
    w = c5 * fact

    # c..compute values at foot of rarefaction
    p3 = p4
    u3 = u4
    rho3 = rho1 * (p3 / p1)**(1. / gamma)

    # c..compute positions of waves
    if pl > pr:
        c1 = math.sqrt(gamma * p1 / rho1)
        c3 = math.sqrt(gamma * p3 / rho3)

        xsh = xi + w * t
        xcd = xi + u3 * t
        xft = xi + (u3 - c3) * t
        xhd = xi - c1 * t

        print('{0}{1}{2}{3}'.format('Region'.center(10), 'Density'.center(10),
                                    'Pressure'.center(10), 'Velocity'.center(10)))
        print('{0}{1}{2}{3}'.format('1'.center(10), repr(rho1).center(10), repr(p1).center(10), repr(u1).center(10)))
        print('{0}'.format('RAREFACTION'.center(20)))
        print('{0}{1:2.4f}\t{2:.4f}\t{3:.4f}'.format('3'.center(10), rho3, p3, u3))
        print('{0}{1:2.4f}\t{2:.4f}\t{3:.4f}'.format('4'.center(10), rho4, p4, u4))
        print('{0}{1:2.4f}\t{2:.4f}\t{3:.4f}'.format('5'.center(10), rho5, p5, u5))
        print('Head of Rarefaction: x = {0}'.format(xhd))
        print('Foot of Rarefaction: x = {0}'.format(xft))
        print('Contact Discontinuity : x = {0}'.format(xcd))
        print('Shock : x = {0}'.format(xsh))


        dx = (xr - xl) / (npts - 1)
        x_arr = np.arange(xl, xr, dx)
        rho_arr = np.zeros(npts, dtype=float)
        p_arr = np.zeros(npts, dtype=float)
        u_arr = np.zeros(npts, dtype=float)

        for x, rho, p, u in zip(x_arr, rho_arr, p_arr, u_arr):
            if x < xhd:
                rho = rho1
                p = p1
                u = u1
            elif x < xft:
                u = 2. / gp1 * (c1 + (x - xi) / t)
                fact = 1. - 0.5 * gm1 * u / c1
                rho = rho1 * fact ** (2. / gm1)
                p = p1 * fact ** (2. * gamma / gm1)
            elif x < xcd:
                rho = rho3
                p = p3
                u = u3
            elif x < xsh:
                rho = rho4
                p = p4
                u = u4
            else:
                rho = rho5
                p = p5
                u = u5

    if pr > pl:
        c1 = math.sqrt(gamma * p1 / rho1)
        c3 = math.sqrt(gamma * p3 / rho3)

        xsh = xi - w * t
        xcd = xi - u3 * t
        xft = xi - (u3 - c3) * t
        xhd = xi + c1 * t

        # c..and do say what we found
        print('{0}{1}{2}{3}'.format('Region'.center(10), 'Density'.center(10),
                                    'Pressure'.center(10), 'Velocity'.center(10)))
        print('{0}{1:2.4f}\t{2:.4f}\t{3:.4f}'.format('1'.center(10), rho5, p5, u5))
        print('{0}{1:2.4f}\t{2:.4f}\t{3:.4f}'.format('2'.center(10), rho4, p4, u4))
        print('{0}{1:2.4f}\t{2:.4f}\t{3:.4f}'.format('3'.center(10), rho3, p3, u3))
        print('{0}'.format('RAREFACTION'.center(20)))
        print('{0}{1:2.4f}\t{2:.4f}\t{3:.4f}'.format('5'.center(10), rho1, p1, u1))

        print('Shock : x = {0}'.format(xsh))
        print('Contact Discontinuity : x = {0}'.format(xcd))
        print('Foot of Rarefaction: x = {0}'.format(xft))
        print('Head of Rarefaction: x = {0}'.format(xhd))

        dx = (xr - xl) / (npts - 1)
        x_arr = np.arange(xl, xr, dx)
        rho_arr = np.zeros(npts, dtype=float)
        p_arr = np.zeros(npts, dtype=float)
        u_arr = np.zeros(npts, dtype=float)

        for x, rho, p, u in zip(x_arr, rho_arr, p_arr, u_arr):
            if x < xsh:
                rho = rho5
                p = p5
                u = -u1
            elif x < xcd:
                rho = rho4
                p = p4
                u = -u4
            elif x < xft:
                rho = rho3
                p = p3
                u = -u3
            elif x < xhd:
                u = -2. / gp1 * (c1 + (xi - x) / t)
                fact = 1. + 0.5 * gm1 * u / c1
                rho = rho1 * fact ** (2. / gm1)
                p = p1 * fact ** (2. * gamma / gm1)
            else:
                rho = rho1
                p = p1
                u = -u1
