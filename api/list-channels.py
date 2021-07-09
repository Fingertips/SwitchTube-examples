"""Use the SWITCHtube web service API to list channels you can contribute to.

Assuming the access token `Hbmqqdc8x49Qjk1L3BKBAec`, list the channels you
can contribute to:

    $ python3 list-channels.py Hbmqqdc8x49Qjk1L3BKBAec

This script is intended to illustrate usage of the SWITCHtube web service API
and is provided “as is”. Please see https://tube.switch.ch/api.html for more
information.

It depends on the Requests HTTP library. On most systems, this can be installed
using `python3 -m pip install requests`.

In case of a "SSLCertVerificationError", run `pip install --upgrade certifi` to
update the CA bundle.
"""

import argparse
import requests

ORIGIN = 'https://tube.switch.ch'

# Define and parse command line arguments.
parser = argparse.ArgumentParser(
    description='List the channels you own on SWITCHtube.')
parser.add_argument('token', help='access token from your SWITCHtube profile')
arguments = parser.parse_args()

# Get channels and show their id and title.
response = requests.get(
    ORIGIN + '/api/v1/channels?role=contributor',
    headers={'Authorization': 'Token ' + arguments.token}
    )
for channel in response.json():
    print("{id}: {name}".format(id=channel['id'], name=channel['name']))
