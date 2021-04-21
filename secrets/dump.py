#!/usr/bin/env python3

"""Load the TOML configuration as a basic syntax validation."""

import sys
import toml


def main(args):
    with open('passwords.toml') as f:
        data = toml.load(f)
    for section, params in data.items():
        print(section)
        for field in ['user', 'password', 'url']:
            value = params.get(field)
            if value:
                print("* {}: {}".format(field, value))


if __name__ == '__main__':
    main(sys.argv)
