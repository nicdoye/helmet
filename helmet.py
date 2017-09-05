#!/usr/bin/env python3

import argparse
import lxml.etree as etree
import re
import requests
import string


# Could get command line
default_repo_url = 'https://kubernetes-charts.storage.googleapis.com/'


def update_latest_version(latest_version_dict, software, version):
    """
    Update the version in the dictionary to the latest version (or set it if it wasn't already present)
    """
    # Add it if it's not in the dictionary. If it is in the dictionary, update
    # if it's a newer version
    if (software not in latest_version_dict) or (version > latest_version_dict[software]):
        latest_version_dict[software] = version


def is_valid_entry(split_chart_entry):
    """
    If the Key doesn't isn't foo-bar-n.m.l.tgz then, it's not software.
    Although we are only checking for the '-n' part
    """
    return(len(split_chart_entry) == 2)


def get_charts(repo_url):
    """
    Read XML from repo
    """
    r = requests.get(repo_url)
    return(r.content)


def get_chart_xml_tree(raw_xml):
    """
    Turn XML intro tree object
    """
    return(etree.XML(raw_xml))


def get_software_version_pair(split_chart_entry, chart_entry):
    """
    Turn valid string into pair
    """
    software = split_chart_entry[0]
    version = re.sub(software + '-', '', chart_entry, count=1)
    version = re.sub('.tgz$', '', version, count=1)
    return(software, version)


def read_charts(tree):
    """
    Loop through all the XML looking for the latest version of each chart
    """
    latest_version_dict = {}
    for chart in tree.findall('{http://doc.s3.amazonaws.com/2006-03-01}Contents'):
        chart_entry = chart.find(
            '{http://doc.s3.amazonaws.com/2006-03-01}Key').text
        split_chart_entry = re.split('-\d', chart_entry, maxsplit=1)
        if is_valid_entry(split_chart_entry):
            software, version = get_software_version_pair(
                split_chart_entry, chart_entry)
            update_latest_version(latest_version_dict, software, version)
    return(latest_version_dict)


def dump_dict(str_str_dict):
    """
    Print all elements of the dictionary
    """
    for key, value in str_str_dict.items():
        print('{} {}'.format(key, str_str_dict[key]))


def main():
    tree = get_chart_xml_tree(get_charts(default_repo_url))
    latest_version_dict = read_charts(tree)
    dump_dict(latest_version_dict)

if __name__ == "__main__":
    # execute only if run as a script
    main()
