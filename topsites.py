#!/usr/bin/env/ python

"""query requests to alexa top sites web service
usage: python topsites.py --auth AUTH_FILE [--country XX] [--country XX]
"""

__author__ = "Vaibhav Bajpai (contact@vaibhavbajpai.com)"
__date__ = "$Date: 2012/12/16 15:45:39 $"
__copyright__ = "Copyright (c) 2012 Vaibhav Bajpai"
__license__ = "Python"

import requests
import datetime
import hmac
import hashlib
import base64
import collections
import xml.etree.ElementTree as ET
import yaml
import argparse

"""Base constant setup"""
HOST = 'ats.amazonaws.com'
ACTION = 'TopSites'
TIMESTAMP = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
RESPONSE_GROUP = "Country"
START = 1
COUNT = 100
SIGNATURE_VERSION = 2
SIGNATURE_METHOD = 'HmacSHA256'

access_key_id = None
country_code = ''


def http_get(access_key_id, secret_access_key, country_code='', signature=''):
    """sends a HTTP GET to alexa top sites web service using requests;
     parses the XML response using xml; filters the response XML for domain
     names and returns the list of domain entries"""

    query = {
        "Action"           : ACTION,
        "AWSAccessKeyId"   : access_key_id,
        "Timestamp"        : TIMESTAMP,
        "ResponseGroup"    : RESPONSE_GROUP,
        "Start"            : START,
        "Count"            : COUNT,
        "CountryCode"      : country_code,
        "SignatureVersion" : SIGNATURE_VERSION,
        "SignatureMethod"  : SIGNATURE_METHOD
    }

    query = collections.OrderedDict(sorted(query.items()))
    req = requests.Request(
                            method='GET',
                            url='http://%s' % HOST,
                            params=query
                          )
    try:
        prep = req.prepare()
    except Exception as e:
        print e

    string_to_sign = '\n'.join([prep.method, HOST, '/', prep.path_url[2:]])
    print(string_to_sign)
    signature = hmac.new(
        key=secret_access_key,
        msg=bytes(string_to_sign),
        digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(signature)
    prep.url = '%s&Signature=%s'%(prep.url, signature)

    s = requests.Session()
    try:
        res = s.send(prep)
    except Exception as e:
        print e
    else:
        try:
            if res.status_code is not requests.codes.ok:
                res.raise_for_status()
        except Exception as e:
            print e
            print res.text

    xml = res.text
    entries = []
    NSMAP = {'aws': 'http://ats.amazonaws.com/doc/2005-11-21'}
    try:
        tree = ET.fromstring(xml)
        xml_elems = tree.findall('.//aws:DataUrl', NSMAP)
        entries = [entry.text for entry in xml_elems]
    except Exception as e:
        print e

    return entries


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Fetches Top 100 sites per country "
                                     "from Alexa Top Sites")
    parser.add_argument('--auth', type=str, required=False, default='auth.yaml',
                        help="YAML file with the access credentials")
    parser.add_argument('--country', type=str, nargs='+', required=True,
                        help="Country to fetch Top 100 sites from")
    args = parser.parse_args()

    """Read the auth credentials"""
    with open(args.auth, 'r') as f:
        auth = yaml.load(f)

    for country in args.country:
        try:
            print("Country: %s" % country)
            for entry in http_get(auth['access_key_id'],
                                  auth['secret_access_key'], country):
                print entry
        except TypeError as e:
            print e
