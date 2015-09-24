# flickr-dumpr
Downloads all of your flickr albums (original photo/video files). Requires Python 2.7 with the [flickrapi](https://pypi.python.org/pypi/flickrapi) module.

### Usage instructions

1. Install the Python Flickr API: https://pypi.python.org/pypi/flickrapi
2. Verify that **everyone** can download the originals from your Flickr account [here](http://www.flickr.com/account/prefs/downloads/?from=privacy).
3. Configure your `USER_ID` in the python script. If you don't know your ID, you can get it [here](http://idgettr.com/).
4. Configure `DOWNLOAD_DIR` in the python script (optional).

Run the python script:

    python flickr-dumpr.py
