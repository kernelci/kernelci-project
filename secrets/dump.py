#!/usr/bin/env python3

"""Load the TOML configuration as a basic syntax validation."""

import sys
import toml


def main(args):
    with open('passwords.toml') as f:
        data = toml.load(f)
    print("Keys: {}".format(list(data.keys())))
    print("All good.")


if __name__ == '__main__':
    main(sys.argv)
