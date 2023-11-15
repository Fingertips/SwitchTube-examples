# Switch Tube usage examples

Usage examples of the [Switch Tube web service API](http://tube.switch.ch/help/api) and the [Switch Tube JavaScript embed library](http://tube.switch.ch/help/embed).

## Web service API

- [download-channel.py](api/download-channel.py) is a Python script that illustrates basic usage of the web service. It allows you to downloading all video from a given channel using an access token from your Switch Tube profile.
- [list-channels.py](api/list-channels.py) list channels you can contribute to.
- [upload.py](api/upload.py) allows you to upload a video to a channel you can contribute to.

## JavaScript embed library

- [Add and control player](embed/add_player.html) shows how to use the embed library to add a video player inside an existing container element on your page, and how to control playback. This is the preferred way to use the embed library from your JavaScript code. You can also view a [live demo of this example](http://embed-examples.fngtps.com/add_player.html).
- [Control existing iframe](embed/control_existing_iframe.html) uses the embed library to control playback for a video embedded using the HTML embed code from a Switch Tube video page. You can also view a [live demo of this example](http://embed-examples.fngtps.com/control_existing_iframe.html).
