# flickr-dumpr
Downloads all of your flickr albums (original photo/video files). Requires Python 2.7 with the [flickrapi](https://pypi.python.org/pypi/flickrapi) module.

### Usage instructions

1. Install the [Python Flickr API](https://pypi.python.org/pypi/flickrapi), e.g. via [pip](https://pip.pypa.io/en/stable/installing/): `pip install -U flickrapi`
2. Verify that **everyone** can download the originals from your Flickr account [here](http://www.flickr.com/account/prefs/downloads/?from=privacy).
3. Configure your `USER_ID` in the python script. If you don't know your ID, you can get it [here](http://idgettr.com/).
4. Configure `DOWNLOAD_DIR` in the python script (optional).

Run the python script:

    python flickr-dumpr.py

### Known issues and limitations

* There is currently no way of retrieving the original file extension for videos. AFAIK this is a [limitation in the API](https://www.flickr.com/groups/51035612836@N01/discuss/72157621698855558/). Therefore, ".mov" is being appended to all video file names, regardless of which extension the should really have.
* You cannot cherry-pick albums to download. This script downloads all albums associated with your Flickr account. However, it will skip existing images which have already been downloaded.
* You will end up with duplicate files if you have assigned the same photo/video to more than one album. That same file will download into each album folder.
* No log file is being created.
* If you don't have any albums, you need to go into Flickr's [organizr](https://www.flickr.com/photos/organize) and put all of your photos into an album.
