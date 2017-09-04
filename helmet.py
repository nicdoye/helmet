#!/usr/bin/env python3

import lxml.etree as etree
import requests
import string
import re

charts = 'https://kubernetes-charts.storage.googleapis.com/'
r = requests.get(charts)

tree = etree.XML(r.content)

latest_version = {}
for chart in tree.findall('{http://doc.s3.amazonaws.com/2006-03-01}Contents'):
    chart_key = chart.find('{http://doc.s3.amazonaws.com/2006-03-01}Key').text
    chart_parts = re.split('-\d', chart_key, maxsplit=1)
    if len(chart_parts) == 2:
        software = chart_parts[0]
        version = re.sub( software + '-' , '', chart_key, count = 1 )
        version = re.sub( '.tgz$', '', version, count = 1)

        # Check if already in dictionary
        if software in latest_version:
            # Check if this a newer version
            if version > latest_version[software]:
                latest_version[software] = version
        else:
            latest_version[software] = version
        
        
for software in latest_version:        
    print('{} {}'.format(software, latest_version[software]))

