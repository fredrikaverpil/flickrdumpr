
import json, urllib, os, sys, datetime, time, logging.config

# Config
USER_ID = u'130608600@N05' # This is the ID for http://www.flickr.com/photos/spacexphotos/
DOWNLOAD_DIR = os.path.dirname(os.path.realpath(__file__)) + '/flickrdumpr'
LOG_FILEPATH = os.path.dirname(os.path.realpath(__file__)) + '/flickrdumpr/flickrdumpr.log'
DISABLE_EXISTING_LOGGERS = True # disables loggers from e.g. the Flickr API


# Flickr API
API_KEY = u'9ef13e2a43de8882ff30fa662a9e98f8'
API_SECRET = u'0f22b5777e4eb262'
FLICKR_API_FOUND = None



try:
    import flickrapi
    FLICKR_API_FOUND = True
except ImportError:
    FLICKR_API_FOUND = False

def check_requirements():
    ''' Makes sure that we have access to the flickr API and will abort the
    script if we can't find it '''
    if not FLICKR_API_FOUND:
        print '''Error: Flickr API not installed/available.
        More info at: https://pypi.python.org/pypi/flickrapi'''
        # More info:
        # https://pypi.python.org/pypi/flickrapi
        # http://stuvel.eu/flickrapi
        return False
    else:
        return True



class FlickrDumpr(object):
    """docstring for ClassName"""
    def __init__(self):
        super(FlickrDumpr, self).__init__()

        self.setup_logging()
        self.setup_flickrapi()
        albums = self.get_albums()
        albums = self.get_media(albums=albums)
        self.download_manager(albums=albums)

    def setup_logging(self):
        log_dir = os.path.dirname(LOG_FILEPATH)
        self.create_dir( path=log_dir ) # create log dir
        if not os.path.exists(LOG_FILEPATH):
            open(LOG_FILEPATH, 'a').close() # create the log file
        
        # Logging
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': DISABLE_EXISTING_LOGGERS,
            'formatters': {
                'formatter': {
                    'format': '%(asctime)s %(levelname)s %(message)s',
                },
            },
            'handlers': {
                'stderr': {
                    'class': 'logging.StreamHandler',
                    'stream' :  sys.stderr,
                    'formatter': 'formatter',
                    'level': 'INFO',
                },
                'log_file': {
                    'class': 'logging.FileHandler',
                    'filename': LOG_FILEPATH,
                    'mode': 'a',
                    'formatter': 'formatter',
                    'level': 'WARNING',
                },
            },
            'loggers': {
                '': {
                    'level': 'INFO',
                    'handlers': ['stderr', 'log_file'],
                },
            },
        })

        self.logger = logging.getLogger('flickrdumprloggr')



    def setup_flickrapi(self):
        ''' API objects '''
        self.logger.info('Creating API objects...')
        self.flickrapi_json = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='json')
        #self.flickrapi_etree = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='etree')
        self.flickrapi_json.authenticate_via_browser(perms='read')

    def get_albums(self):
        ''' Creates an albums dictionary '''
        self.logger.info('Retrieving album list...')
        response_string = self.flickrapi_json.photosets.getList(user_id=USER_ID, extras='original_format,url_o')
        json_data = json.loads( response_string )
        albums = {}
        for album in json_data['photosets']['photoset']:
            if 'title' in album.keys():
                title = album['title']['_content']
                set_id = album['id']
                albums[set_id] = { 'title' : title,
                                    'media' : {}
                                 }
        return albums

    def get_video_details(self, media_id):
        ''' Fetches the link to the original video file '''
        response_string = self.flickrapi_json.photos.getSizes(photo_id=media_id, user_id=USER_ID)
        json_data = json.loads( response_string )
        for size in json_data['sizes']['size']:
            if 'label' in size:
                video_label = size['label']
                if 'Video Original' in video_label:
                    url_original_format = size['source']
                    return url_original_format

    def get_media(self, albums):
        ''' Adds photo/video information into the albums dictionary '''
        album_count = 1
        for album_id in albums:
            album_title_validated = self.validate_string( string=albums[album_id]['title'] )
            page = 1
            photos = []
            videos = []
            items = [] # number of items (photos AND videos)
            logger_msg = 'Indexing album (' + str(album_count) + '/' + str(len(albums)) + '): ' + albums[album_id]['title']
            self.logger.info( logger_msg )
            

            while ( len(items) == 500 or page == 1 ):
                response_string = self.flickrapi_json.photosets.getPhotos(photoset_id=album_id, user_id=USER_ID, extras='original_format, url_o, media', page=str(page) )
                json_data = json.loads( response_string )   
                
                media = json_data['photoset']['photo']
                for m in media:
                    media_id = m['id']
                    media_title = m['title']
                    media_type = m['media']
                    if media_type == 'photo':
                        url_original_format = m['url_o']
                        dst_filename = os.path.basename( url_original_format )
                        photos.append(m)
                    elif media_type == 'video':
                        url_original_format = self.get_video_details(media_id=media_id)
                        dst_filename = m['id'] + '.mov' # hardcoded .mov :(
                        videos.append(m)
                    else:
                        logger_msg = 'Unsupported media detected: ' + media_type + ': ' + media_title + ' of album ' + album_title_validated + ' (skipping download)'
                        self.logger.warning( logger_msg )
                    
                    items.append(m)
                    if type(url_original_format) == type(None):
                        logger_msg = 'No download URL found for ' + str(media_id) + ' ' + media_title + ' of album ' + album_title_validated + ' (skipping download)'
                        self.logger.warning( logger_msg )

                    else:
                        albums[album_id]['media'][media_id] =   {
                                                                    'media_type' : media_type,
                                                                    'url_original_format' : url_original_format,
                                                                    'dst_filename' : dst_filename
                                                                }



                page += 1


            album_count += 1
            if len(photos ) > 0:
                logger_msg = 'Found ' + str(len(photos)) + ' photos'
                self.logger.info( logger_msg )
            if len(videos) > 0:
                logger_msg = 'Found ' + str(len(videos)) + ' videos'
                self.logger.info( logger_msg )

        return albums



    def downloader(self, url, dst):
        ''' Download link "url" and save as "dst" '''
        try:
            urllib.urlretrieve( url, dst )
            return True
        except:
            return False


    def validate_string(self, string):
        ''' Validates a string so that it can be used as a folder name or file name '''
        string = string.replace('/', '-')
        string = string.replace('\\', '-')
        string = string.replace(' ', '_')
        return string


    def create_dir(self, path):
        ''' Create the download dir unless it already exists '''
        if not os.path.exists(path):
            os.makedirs(path)

    def download_manager(self, albums):
        ''' Fetch the albums dictionary with photo/video information, then download each photo into an album folder '''
        retries = 0
        skipped = 0
        successful_downloads = 0

        album_count = 1
        for album_id in albums:
            logger_msg = 'Downloading album (' + str(album_count) + '/' + str(len(albums)) + '): ' + albums[album_id]['title'] + '...'
            self.logger.info( logger_msg )
            media_count = 1
            for media_id in albums[album_id]['media']:
                m = albums[album_id]['media'][media_id]
                media_type = m['media_type']
                album_title_validated = self.validate_string( string=albums[album_id]['title'] )
                dst_dir = DOWNLOAD_DIR + '/' + album_title_validated
                self.create_dir( path=dst_dir )
                tmp_filepath = dst_dir + '/' + 'flickrdumpr_temp'
                dst_filepath = dst_dir + '/' + m['dst_filename']
                
                if not os.path.exists(dst_filepath):
                    downloaded = False
                    while not downloaded:
                        time.sleep(1)
                        logger_msg = 'Downloading ' + media_type + ' (' + str(media_count) + '/' + str(len(albums[album_id]['media'])) +  '): ' + m['url_original_format']
                        self.logger.info( logger_msg )
                        downloaded = self.downloader( url=m['url_original_format'], dst=tmp_filepath )
                        if downloaded:
                            os.rename(tmp_filepath, dst_filepath)
                            successful_downloads += 1
                        else:
                            logger_msg = 'Retrying (indefinitively), ' + media_type + ': ' + m['url_original_format'] + ' of album ' + album_title_validated
                            retries += 1
                            self.logger.error( logger_msg )
                else:
                    logger_msg = 'Skipping ' + media_type + ' (' + str(media_count) + '/' + str(len(albums[album_id]['media'])) + '): ' + m['url_original_format']
                    skipped += 1
                    self.logger.info( logger_msg )

                media_count += 1
            album_count +=1

        logger_msg = '\n\nAll downloads completed!\nSummary:\nSuccessful photo/video downloads: ' + str(successful_downloads) + '\nSkipped photo/video downloads: ' + str(skipped) + '\nNumber of retries: ' + str(retries) + '\nCheck log file for additional warnings and errors: ' + LOG_FILEPATH
        self.logger.info( logger_msg )


if __name__ == '__main__':
    if check_requirements():
        FlickrDumpr()
