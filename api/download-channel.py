"""Download all video from a channel using the Switch Tube web service API.

Assuming the access token `Hbmqqdc8x49Qjk1L3BKBAec`, download all video from
the channel with id `c61x4b` to a directory named `videos` by running:

    $ python3 download-channel.py Hbmqqdc8x49Qjk1L3BKBAec c61x4b ./videos

This script is intended to illustrate usage of the Switch Tube web service API
and is provided “as is”. Please see https://tube.switch.ch/api.html for more
information.

It depends on the Requests HTTP library. On most systems, this can be installed
using `python3 -m pip install requests`.

It also depends on the pathvalidate library to sanitize filenames. This can be
installed using `python3 -m pip install pathvalidate`.

In case of a "SSLCertVerificationError", run `pip install --upgrade certifi` to
update the CA bundle.
"""

import argparse
import pathlib
import requests
import pathvalidate

ORIGIN = 'https://tube.switch.ch'


def truncate(string, length=60):
    """Truncate the given string when it exceeds the given length."""
    return string[:length - 4] + '.' * 3 if len(string) > length else string


def get(url):
    """Return response data and URL for the next page given a URL.

    The returned URL will be `None` when there is no next page.
    """
    # Build the auth header using the access token command line argument.
    headers = {'Authorization': 'Token ' + arguments.token}
    # GET from the URL. Include the auth header with the request.
    response = requests.get(url, headers=headers)
    # Stop and show a message when the response has an error status code.
    response.raise_for_status()
    # Try to get a the link to the next page.
    next_link = response.links.get('next')
    # Return the decoded data and a URL for the next page (if available).
    return (response.json(), next_link and next_link.get('url'))


def download(url, path):
    """Request the given url and save the response to the local path."""
    # GET from the URL. Tell the HTTP library to stream instead of loading the
    # entire response body in-memory.
    response = requests.get(url, stream=True)
    # Stop and show a message when the response has an error status code.
    response.raise_for_status()
    # Set the size of the chunks to download in bytes.
    chunk_size = 16384
    # Use the size of the response body to calculate the number of chunks to
    # download. This will be used to show download progress.
    number_of_chunks = int(response.headers['Content-Length']) / chunk_size
    # Keep track of the number of chunks downloaded to show download progress.
    chunks_downloaded = 0
    # Open the local file to save the downloaded data to.
    with open(path, 'wb') as fd:
        # Loop through the chunks as they’re downloading.
        for chunk in response.iter_content(chunk_size=chunk_size):
            # Write the chunk to the local file.
            fd.write(chunk)
            # Increase the number of chunks downloaded.
            chunks_downloaded += 1
            # Show the filename and the download progress as a percentage.
            print("{filename} {progress}%".format(
                filename=truncate(path.name),
                progress=round(chunks_downloaded / number_of_chunks * 100)
                ), end="\r", flush=True)
    print("{} 100%".format(truncate(path.name)))


# Define and parse command line arguments.
parser = argparse.ArgumentParser(
    description='Download all video from a Switch Tube channel.')
parser.add_argument('token', help='access token from your Switch Tube profile')
parser.add_argument('channel', help='id of the channel')
parser.add_argument(
    'target_directory', type=pathlib.Path, help='directory to download to')
arguments = parser.parse_args()

# When a channel contains a lot of videos, its video listing will be split over
# multiple “pages” as explain in https://tube.switch.ch/api.html#pagination

# Create a URL to list videos using the channel id command line argument.
videos_url = ORIGIN + \
    '/api/v1/browse/channels/{}/videos'.format(arguments.channel)
# Loop as long as there’s a URL.
while videos_url:
    # Get the listed videos and a URL for the next page (if available).
    videos, videos_url = get(videos_url)
    # Loop through the returned videos.
    for video in videos:
        # Create a URL to list the available variants using the video id.
        variants_url = ORIGIN + \
            '/api/v1/browse/videos/{}/video_variants'.format(video['id'])
        # Get the available video variants. The next page URL can be ignored as
        # only the first variant will be used (the number of variants is also
        # unlikely to exceed the page size anytime soon).
        variants, _ = get(variants_url)
        # Skip over audio-only media.
        if variants:
            # Create a filename from the video id and title. Currently, all
            # encoded variants use the MP4 container format.
            filename = video['id'] + '-' + video['title'] + '.mp4'
            # Build a local filesystem path to save the downloaded file to
            # using the target directory command line argument.
            path = arguments.target_directory / \
                pathvalidate.sanitize_filename(filename)
            # Variants are ordered on quality level with the highest quality
            # variant listed first. Create the URL to the first variant.
            variant_url = ORIGIN + variants[0]['path']
            # Download from the variant URL path to the local filesystem path.
            download(variant_url, path)
