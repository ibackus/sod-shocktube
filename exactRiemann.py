
import sod
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    gamma = 1.4
    npts = 500

    # left_state and right_state set p, rho and u
    # geometry sets left boundary on 0., right boundary on 1 and initial
    # position of the shock xi on 0.5
    # t is the time evolution for which positions and states in tube should be calculated
    # gamma denotes specific heat
    # note that gamma and npts are default parameters (1.4 and 500) in solve function
    positions, regions, values = sod.solve(left_state=(1, 1, 0), right_state=(0.1, 0.125, 0.),
                                           geometry=(0., 1., 0.5), t=0.2, gamma=gamma, npts=npts)
    # Printing positions
    print('Positions:')
    for desc, vals in positions.items():
        print('{0:10} : {1}'.format(desc, vals))

    # Printing p, rho and u for regions
    print('Regions:')
    for region, vals in sorted(regions.items()):
        print('{0:10} : {1}'.format(region, vals))

    # Create energy and temperature
    E = values['p']/(gamma-1.) + 0.5*values['u']**2
    T = values['p']/values['rho']
    # Mach number: u/c
    M = values['u']/np.sqrt(values['p']/values['rho'])

    # and add them to previous results
    values.update({"E": E, "T": T, "M": M})

    # Finally, let's plot the solutions
    plt.close('all')
    f, axarr = plt.subplots(len(values)-1, sharex=True)

    axarr[0].plot(values['x'], values['p'], linewidth=1.5, color='b')
    axarr[0].set_ylabel('pressure')
    axarr[0].set_ylim(0, 1.1)

    axarr[1].plot(values['x'], values['rho'], linewidth=1.5, color='r')
    axarr[1].set_ylabel('density')
    axarr[1].set_ylim(0, 1.1)

    axarr[2].plot(values['x'], values['u'], linewidth=1.5, color='g')
    axarr[2].set_ylabel('velocity')

    axarr[3].plot(values['x'], values['E'], linewidth=1.5, color='k')
    axarr[3].set_ylabel('energy')
    axarr[3].set_ylim(0, 2.6)

    axarr[4].plot(values['x'], values['T'], linewidth=1.5, color='c')
    axarr[4].set_ylabel('temperature')

    axarr[5].plot(values['x'], values['M'], linewidth=1.5, color='y')
    axarr[5].set_ylabel('Mach number')

    plt.show()