# flickr-dumpr
Downloads all of your flickr albums (original photo/video files). Requires Python 2.7 with the [flickrapi](https://pypi.python.org/pypi/flickrapi) module.

### Usage instructions

1. Install the [Python Flickr API](https://pypi.python.org/pypi/flickrapi), e.g. via [pip](https://pip.pypa.io/en/stable/installing/): `pip install -U flickrapi`
2. Verify that "**everyone**" can download the originals from your Flickr account [here](http://www.flickr.com/account/prefs/downloads/?from=privacy).
3. Configure your `USER_ID` in the python script. If you don't know your ID, you can get it [here](http://idgettr.com/).
4. Configure `DOWNLOAD_DIR` in the python script (optional).

Run the python script:

    python flickr-dumpr.py

The first time you run the script, a web browser window should open and you will be prompted to authorize the flickr-dumpr script to get read-only access to your Flickr account.

You can cancel the script exection at any time using **Ctrl + c**.


### Known issues and limitations

* There is currently no way of retrieving the original file extension for videos. AFAIK this is a [limitation in the API](https://www.flickr.com/groups/51035612836@N01/discuss/72157621698855558/). Therefore, ".mov" is being appended to all video filenames, regardless of which extension the should really have.
* You cannot cherry-pick albums to download. This script downloads all albums associated with your Flickr account. However, it will skip existing photos and videos which have already been downloaded.
* You will end up with duplicate files if you have assigned the same photo/video to more than one album. That same file will download into each album folder.
* No log file is being created.
* If you don't have any albums, you need to go into Flickr's [organizr](https://www.flickr.com/photos/organize) and put all of your photos into an album.

### FAQ

> Why did you make this?

Because the regular way of downloading albums don't always work. Read more [here]( https://www.flickr.com/help/forum/en-us/72157654124474892/).

> Can I end up with incompleted downloads?

There's always a risk. However, each photo/video is downloaded as a temp file. Not until it is completely downloaded it is renamed into the actual filename on disk. So at least in theory, if you cancel the script operation and re-run it, you should not have to worry about incompleted downloads. I've downloaded tens of thousands of photos/videos using this script and it has never produced incompleted files for me (fingers crossed).

> How do I keep track of any failed downloads?

Each download is retried indefinitely until it is completely downloaded. If a download seems to never finish, you can cancel the operation (**Ctrl + c**) and re-run the script. I am going to implement a log file which will show you all warnings during the script operation, such as if the script is unable to successfully fetch the download URL for a photo/video (a very rare case, and usually stems from an error on Flickr's side).

> One of my photos says "This photo is no longer available". What's going on?

I've noticed this on very rare occasions too. Have a look in the Flickr help forums: https://www.flickr.com/help/forum/en-us/72157649823558847/

> I don't see a license anywhere. You must decide on a license!

You can do whatever you like with this script. But I cannot be held responsible for whatever it is you do. Having that said, it would be nice of you to contribute back if you make any improvements to this script.
