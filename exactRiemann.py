import sod


if __name__ == '__main__':
    sod.solve(left_state=(1, 1, 0), right_state=(0.1, 0.125, 0.),
              geometry=(0., 1., 0.5), t=0.2)

