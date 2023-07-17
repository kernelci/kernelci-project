#!/usr/bin/env python3
#
# SPDX-License-Identifier: LGPL-2.1-or-later
#
# Copyright (C) 2023 Collabora Limited
# Author: Guillaume Tucker <guillaume.tucker@collabora.com>

"""Azure sponsorship usage parser"""

import argparse
import datetime
import json

COLORS = {
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'blue': '\033[94m',
    'bold': '\033[1m',
    'underline': '\033[4m',
    'clear': '\033[0m',
}


def _color(msg, color):
    return ''.join([COLORS[color], msg, COLORS['clear']])


def _bold(msg):
    return _color(msg, 'bold')


def _under(msg):
    return _color(msg, 'underline')


class Usage:
    """Usage data parser

    This class takes the raw JSON data with the Azure subscription usage and
    provides methods for analysing it.  The sub_id optional argument is to
    filter data for only one subscription GUID.
    """

    def __init__(self, usage, sub_id=None):
        self._usage = usage
        self._sub_id = sub_id
        if self._sub_id:
            self._usage = list(self._filter_by_subscription())

    def __getitem__(self, index):
        return self._usage[index]

    def __len__(self):
        return len(self._usage)

    def _filter_by_subscription(self):
        for entry in self._usage:
            if entry['SubscriptionGuid'] == self._sub_id:
                yield entry

    @property
    def subscription_guid(self):
        """Azure subscription GUID"""
        return self._sub_id

    @classmethod
    def from_json(cls, json_path, sub_id=None):
        """Create a Usage object from a JSON file path"""
        with open(json_path, encoding='utf-8') as usage_file:
            return Usage(json.load(usage_file), sub_id)

    def by_date(self):
        """Get the data in a dictionary with dates as keys"""
        usage_by_date = {}
        for entry in self._usage:
            when = datetime.datetime.fromisoformat(entry['Date'])
            usage_data = usage_by_date.setdefault(when, [])
            usage_data.append(entry)
        return usage_by_date

    def by_category(self):
        """Get the data in a dictionary with categories as keys"""
        usage_by_cat = {}
        for entry in self._usage:
            cat = usage_by_cat.setdefault(entry['ServiceName'], [])
            cat.append(entry)
        return usage_by_cat

    @classmethod
    def totals(cls, data):
        """Get the total cost for a dictionary of entries"""
        return {
            key: sum(entry['Cost'] for entry in item)
            for key, item in data.items()
        }


def _show_details(usage):
    for when, item in usage.by_date().items():
        date = when.strftime('%Y-%m-%d')
        for entry in item:
            service, resource, region, guid, cost = (
                entry[key] for key in [
                    'ServiceName',
                    'ServiceResource',
                    'ServiceRegion',
                    'ResourceGuid',
                    'Cost'
            ])
            print(f"\
{date} {service:24s} {cost:8.2f}   \
{guid}  {region:18s} {resource}")


def _show_daily_totals(usage, details=True):
    by_date = usage.by_date()
    dates = list(by_date.keys())
    totals = usage.totals(by_date)
    full_total = 0
    dates = sorted(totals.keys())
    for when in dates:
        total = totals[when]
        full_total += total
        if details:
            print(f"{when.strftime('%Y-%m-%d')} {total:8.2f}")
    delta = max(dates) - min(dates)
    average = full_total / (delta.days + 1)
    if details:
        print("-------------------")
    print(f"Total:     {full_total:8.2f}")
    print(f"Average:   {average:8.2f}")


def _show_category_totals(usage):
    totals = usage.totals(usage.by_category())
    swapped = {total: cat for cat, total in totals.items()}
    for total in reversed(sorted(swapped.keys())):
        cat = swapped[total]
        print(f"{cat:24s} {total:8.2f}")


def main(args):
    """Entry point for the command line interface"""
    usage = Usage.from_json(args.usage, args.subscription)
    if args.daily_detail:
        print(_bold("Detailed log:"))
        _show_details(usage)
        print()
    if args.categories:
        print(_bold("Total per category"))
        _show_category_totals(usage)
        print()
    print(_bold("Daily totals"))
    _show_daily_totals(usage, args.daily_totals)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Parse Azure sponsorship costs")
    parser.add_argument(
        'usage',
        help="Path to the JSON Azure usage file"
    )
    parser.add_argument(
        '--subscription',
        default='fd1f9aff-ce5e-4029-93c2-a2fa279f9b9f',
        help="Subscription UUID"
    )
    parser.add_argument(
        '--daily-detail',
        action='store_true',
        help="Show the daily detailed log"
    )
    parser.add_argument(
        '--daily-totals',
        action='store_true',
        help="Show the daily totals"
    )
    parser.add_argument(
        '--categories',
        action='store_true',
        help="Show the total costs per category"
    )
    main(parser.parse_args())
