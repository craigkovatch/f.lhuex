#!/usr/bin/env python3

from pysolar.solar import *
import datetime
import requests
import json
import sys
import warnings

def bridge_ip():
    meethue_page = requests.get('https://www.meethue.com/api/nupnp').json()
    return meethue_page[0]['internalipaddress']

bridge_ip = bridge_ip()
username = "api username goes here"
group = 0
lat = 21.3069
long = -157.8583

def put_request(value):
    r = requests.put('http://{}/api/{}/groups/{}/action'.format(
        bridge_ip, username, group), data=json.dumps(value))

d = datetime.datetime.now()

with warnings.catch_warnings():
	warnings.simplefilter("ignore")
	altitude = get_altitude(lat, long, d)

if altitude <= -18:
    temp = 500
elif altitude >= -18 and altitude < -5:
    temp = 500
elif altitude >= -5 and altitude < -2:
    temp = 320
elif altitude >= -2 and altitude < 0:
    temp = 300
elif altitude >= 0 and altitude < 5:
    temp = 280
elif altitude >= 5 and altitude < 10:
    temp = 270
elif altitude >= 10 and altitude < 20:
    temp = 254
elif altitude >= 20 and altitude < 30:
    temp = 245
elif altitude >= 30 and altitude < 40:
    temp = 234
elif altitude >= 40 and altitude <= 90:
    temp = 153

if len(sys.argv) == 2:
    bri = int(sys.argv[1])
else:
    bri = 100

print("Setting brightness level to {}%...".format(bri))
bri = round(max(min(255,bri*2.55), 0))

if bri > 0:
	put_request({'on': True, 'bri': bri, 'ct': temp})
	print("Set group {} bright {} temp {}".format(group, bri, temp))
else:
	put_request({'on': False, 'ct': temp})
	print("Turned group {} off".format(group))
