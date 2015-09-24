# flickr-dumpr
Downloads all of your flickr albums (original photo/video files). Requires Python 2.7 with the [flickrapi](https://pypi.python.org/pypi/flickrapi) module.

### Usage instructions

1. Install the Python Flickr API: https://pypi.python.org/pypi/flickrapi
2. Verify that **everyone** can download the originals from your Flickr account [here](http://www.flickr.com/account/prefs/downloads/?from=privacy).
3. Configure your `USER_ID` in the python script. If you don't know your ID, you can get it [here](http://idgettr.com/).
4. Configure `DOWNLOAD_DIR` in the python script (optional).

Run the python script:

    python flickr-dumpr.py

### Known issues and limitations

* There is currently no way of retrieving the original file extension for videos. Therefore I append ".mov" to all video files, regardless of which extension the should really have.
* You cannot cherry-pick albums to download. This script downloads all albums associated with your Flickr account. However, it will skip existing images which have already been downloaded.
* You will end up with duplicates if you have assigned the same image to more than one album. That image will download into each album folder.
