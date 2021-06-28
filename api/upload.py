"""Upload a video to a channel using the SWITCHtube web service API.

Assuming the access token `Hbmqqdc8x49Qjk1L3BKBAec`, upload `video.mp4` to the
channel with id `42` using `Maths 101` as its title:

    $ python3 upload.py Hbmqqdc8x49Qjk1L3BKBAec 42 video.mp4 "Maths 101"

This script is intended to illustrate usage of the SWITCHtube web service API
and is provided “as is”. Please see https://tube.switch.ch/api.html for more
information.

It depends on the Requests HTTP library. On most systems, this can be installed
using `python3 -m pip install requests`.

It also depends on a Python client for the tus resumable upload protocol
which can be installed with `python3 -m pip install tus.py`.

In case of a "SSLCertVerificationError", run `pip install --upgrade certifi` to
update the CA bundle.
"""

import argparse
import pathlib
import requests
import tus

ORIGIN = 'https://tube.switch.ch'

# Define and parse command line arguments.
parser = argparse.ArgumentParser(
    description='Upload a video to a SWITCHtube channel.')
parser.add_argument('token', help='access token from your SWITCHtube profile')
parser.add_argument('channel', help='id of the channel')
parser.add_argument('path', type=pathlib.Path, help='file to upload')
parser.add_argument('title', help='video title')
arguments = parser.parse_args()

# Build the auth header using the access token command line argument.
headers = {'Authorization': 'Token ' + arguments.token}

# Upload the file in parts.
with open(arguments.path, 'rb') as fd:
    upload_url = tus.create(
        ORIGIN + '/files',
        arguments.path.name,
        arguments.path.stat().st_size,
        headers=headers
    )
    tus.resume(fd, upload_url, headers=headers)

# Create a new video with the uploaded file.
response = requests.post(
    ORIGIN + '/api/v1/videos',
    headers=headers,
    json={
        'channel_id': arguments.channel,
        # The last path segment of the upload url is the upload identifier.
        'upload_id': upload_url.split('/')[-1],
        'title': arguments.title,
        'published': True
        }
    )
# Stop and show a message when the response has an error status code.
response.raise_for_status()
# Show the URL of the new video.
print(ORIGIN + response.json()['path'])
