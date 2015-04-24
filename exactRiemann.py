import math
import numpy as np
import scipy
import scipy.optimize


def f(p4, p1, p5, rho1, rho5, gamma):
    z = (p4 / p5 - 1.)
    c1 = math.sqrt(gamma * p1 / rho1)
    c5 = math.sqrt(gamma * p5 / rho5)

    gm1 = gamma - 1.
    gp1 = gamma + 1.
    g2 = 2. * gamma

    fact = gm1 / g2 * (c5 / c1) * z / math.sqrt(1. + gp1 / g2 * z)
    fact = (1. - fact) ** (g2 / gm1)

    return p1 * fact - p4


def calculate_regions(pl, ul, rhol, pr, ur, rhor, gamma=1.4):
    """
    Compute regions
    :param pl:
    :param ul:
    :param rhol:
    :param pr:
    :param ur:
    :param rhor:
    :param gamma:
    :return:
    """
    # ..begin solution
    # if pl > pr
    rho1 = rhol
    p1 = pl
    u1 = ul
    rho5 = rhor
    p5 = pr
    u5 = ur

    # unless...
    if pl < pr:
        rho1 = rhor
        p1 = pr
        u1 = ur
        rho5 = rhol
        p5 = pl
        u5 = ul

    # ..solve for post-shock pressure
    p4 = scipy.optimize.fsolve(f, p1, (p1, p5, rho1, rho5, gamma))[0]

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
    return p1, rho1, u1, p3, rho3, u3, p4, rho4, u4, p5, rho5, u5, w


def calc_positions(pl, pr, p1, p3, rho1, rho3, u3, w, xi, t, gamma):
    """
    :return: Head of Rarefaction: xhd,  Foot of Rarefaction: xft,
            Contact Discontinuity: xcd, Shock: xsh}
    """
    c1 = math.sqrt(gamma * p1 / rho1)
    c3 = math.sqrt(gamma * p3 / rho3)
    if pl > pr:
        xsh = xi + w * t
        xcd = xi + u3 * t
        xft = xi + (u3 - c3) * t
        xhd = xi - c1 * t
    else:
        # pr > pl
        xsh = xi - w * t
        xcd = xi - u3 * t
        xft = xi - (u3 - c3) * t
        xhd = xi + c1 * t

    return xhd, xft, xcd, xsh


def region_states(pl, pr, p1, p3, p4, p5, rho1, rho3, rho4, rho5, u1, u3, u4, u5):
    if pl > pr:
        return {'Region 1': (p1, rho1, u1),
                'Region 2': 'RAREFACTION',
                'Region 3': (p3, rho3, u3),
                'Region 4': (p4, rho4, u4),
                'Region 5': (p5, rho5, u5)}
    else:
        return {'Region 1': (p5, rho5, u5),
                'Region 2': (p4, rho4, u4),
                'Region 3': (p3, rho3, u3),
                'Region 4': 'RAREFACTION',
                'Region 5': (p1, rho1, u1)}


def create_arrays(pl, pr, xl, xr, positions, state1, state3, state4, state5, npts, gamma, t, xi):
    (xhd, xft, xcd, xsh) = positions
    (p1, rho1, u1) = state1
    (p3, rho3, u3) = state3
    (p4, rho4, u4) = state4
    (p5, rho5, u5) = state5
    gm1 = gamma - 1.
    gp1 = gamma + 1.

    dx = (xr-xl)/(npts-1)
    x_arr = np.arange(xl, xr, dx)
    rho = np.zeros(npts, dtype=float)
    p = np.zeros(npts, dtype=float)
    u = np.zeros(npts, dtype=float)
    c1 = math.sqrt(gamma * p1 / rho1)
    if pl > pr:
        for i, x in enumerate(x_arr):
            if x < xhd:
                rho[i] = rho1
                p[i] = p1
                u[i] = u1
            elif x < xft:
                u[i] = 2. / gp1 * (c1 + (x - xi) / t)
                fact = 1. - 0.5 * gm1 * u[i] / c1
                rho[i] = rho1 * fact ** (2. / gm1)
                p[i] = p1 * fact ** (2. * gamma / gm1)
            elif x < xcd:
                rho[i] = rho3
                p[i] = p3
                u[i] = u3
            elif x < xsh:
                rho[i] = rho4
                p[i] = p4
                u[i] = u4
            else:
                rho[i] = rho5
                p[i] = p5
                u[i] = u5
    else:
        for i, x in enumerate(x_arr):
            if x < xsh:
                rho[i] = rho5
                p[i] = p5
                u[i] = -u1
            elif x < xcd:
                rho[i] = rho4
                p[i] = p4
                u[i] = -u4
            elif x < xft:
                rho[i] = rho3
                p[i] = p3
                u[i] = -u3
            elif x < xhd:
                u[i] = -2. / gp1 * (c1 + (xi - x) / t)
                fact = 1. + 0.5 * gm1 * u[i] / c1
                rho[i] = rho1 * fact ** (2. / gm1)
                p[i] = p1 * fact ** (2. * gamma / gm1)
            else:
                rho[i] = rho1
                p[i] = p1
                u[i] = -u1

    return x_arr, p, rho, u


def solve_sod(left_state, right_state, geometry, t, gamma=1.4, npts=500):
    """
    Solves the Sod problem (which is a riemann problem) of discontinuity across an interface.

    :param left_state: tuple (pl, rhol, ul)
    :param right_state: tuple (pr, rhor, ur)
    :param geometry: tuple (xl, xr, xi): xl - left boundary, xr - right boundary, xi - initial discontinuity
    :param t: time for which the states have to be calculated
    :param gamma: ideal gas constant, default is air: 1.4
    :param npts: number of points for array of pressure, density and velocity
    :return: tuple of: dicts of positions,
    constant pressure, density and velocity states in distinct regions,
    arrays of pressure, density and velocity in domain bounded by xl, xr
    """

    (pl, rhol, ul) = left_state
    (pr, rhor, ur) = right_state
    (xl, xr, xi) = geometry

    # basic checking
    if xl >= xr:
        print('xl has to be less than xr!')
        exit()
    if xi >= xr or xi <= xl:
        print('xi has in between xl and xr!')
        exit()

    # ..begin solution
    p1, rho1, u1, p3, rho3, u3, p4, rho4, u4, p5, rho5, u5, w = \
        calculate_regions(pl, ul, rhol, pr, ur, rhor, gamma)

    x_positions = calc_positions(pl, pr, p1, p3,
                                 rho1, rho3,
                                 u3, w, xi, t, gamma)
    print(x_positions)

    pos_description = ('Head of Rarefaction', 'Foot of Rarefaction',
                       'Contact Discontinuity', 'Shock')
    positions = dict(zip(pos_description, x_positions))

    for desc, values in positions.items():
        print('{0:10} ==> {1}'.format(desc, values))

    regions = region_states(pl, pr, p1, p3, p4, p5,
                            rho1, rho3, rho4, rho5,
                            u1, u3, u4, u5)

    # for region, values in sorted(regions.items()):
    #    print('{0:10} ==> {1}'.format(region, values))


    x, p, rho, u = create_arrays(pl, pr, xl, xr, x_positions,
                                 (p1, rho1, u1), (p3, rho3, u3),
                                 (p4, rho4, u4), (p5, rho5, u5), npts, gamma, t, xi)

    val_names = ('x', 'p', 'rho', 'u')
    val_dict = dict(zip(val_names, (x, p, rho, u)))

    return positions, regions, val_dict

if __name__ == '__main__':
    solve_sod(left_state=(1, 1, 0), right_state=(0.1, 0.125, 0.),
              geometry=(0., 1., 0.5), t=0.2)

