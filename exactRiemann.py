import sod
import matplotlib.pyplot as plt

if __name__ == '__main__':
    """
    usage example
    """
    gamma = 1.4
    positions, regions, values = sod.solve(left_state=(1, 1, 0), right_state=(0.1, 0.125, 0.),
                                           geometry=(0., 1., 0.5), t=0.2, gamma=gamma)
    # Let's print positions
    print('******')
    for desc, vals in positions.items():
        print('{0:10} ==> {1}'.format(desc, vals))
    print('******')
    # Let's print regions
    for region, vals in sorted(regions.items()):
        print('{0:10} ==> {1}'.format(region, vals))

    p = values['p']
    rho = values['rho']
    u = values['u']

    E = p/(gamma-1.) + 0.5*u**2
    T = p/rho
    plt.figure(1)
    plt.plot(values['x'], p, linewidth=1.5, color='b')
    plt.plot([positions['Head of Rarefaction'], positions['Head of Rarefaction']], [0, 1.1], 'k--')
    plt.plot([positions['Foot of Rarefaction'], positions['Foot of Rarefaction']], [0, 1.1], 'k--')
    plt.plot([positions['Shock'], positions['Shock']], [0, 1.1], 'k--')
    plt.ylabel('pressure')
    plt.xlabel('x')
    plt.axis([0, 1, 0, 1.1])

    plt.figure(2)
    plt.plot(values['x'], rho, linewidth=1.5, color='r')
    plt.plot([positions['Head of Rarefaction'], positions['Head of Rarefaction']], [0, 1.1], 'k--')
    plt.plot([positions['Foot of Rarefaction'], positions['Foot of Rarefaction']], [0, 1.1], 'k--')
    plt.plot([positions['Contact Discontinuity'], positions['Contact Discontinuity']], [0, 1.1], 'k--')
    plt.plot([positions['Shock'], positions['Shock']], [0, 1.1], 'k--')
    plt.ylabel('density')
    plt.xlabel('x')
    plt.axis([0, 1, 0, 1.1])

    plt.figure(3)
    plt.plot(values['x'], u, linewidth=1.5, color='g')
    plt.ylabel('velocity')
    plt.xlabel('x')
    plt.plot([positions['Head of Rarefaction'], positions['Head of Rarefaction']], [0, 1], 'k--')
    plt.plot([positions['Foot of Rarefaction'], positions['Foot of Rarefaction']], [0, 1], 'k--')
    plt.plot([positions['Shock'], positions['Shock']], [0, 1], 'k--')


    plt.figure(4)
    plt.plot(values['x'], E, linewidth=1.5, color='k')
    plt.ylabel('Energy')
    plt.xlabel('x')
    plt.axis([0, 1, 0, 2.6])
    plt.plot([positions['Head of Rarefaction'], positions['Head of Rarefaction']], [0, 2.6], 'k--')
    plt.plot([positions['Foot of Rarefaction'], positions['Foot of Rarefaction']], [0, 2.6], 'k--')
    plt.plot([positions['Shock'], positions['Shock']], [0, 1.1], 'k--')

    plt.figure(5)
    plt.plot(values['x'], T, linewidth=1.5, color='c')
    plt.ylabel('Temperature')
    plt.xlabel('x')
    plt.plot([positions['Head of Rarefaction'], positions['Head of Rarefaction']], [0.6, 1.2], 'k--')
    plt.plot([positions['Foot of Rarefaction'], positions['Foot of Rarefaction']], [0.6, 1.2], 'k--')
    plt.plot([positions['Contact Discontinuity'], positions['Contact Discontinuity']], [0.6, 1.2], 'k--')
    plt.plot([positions['Shock'], positions['Shock']], [0.6, 1.2], 'k--')
    plt.axis([0, 1, 0.7, 1.2])
    plt.show()