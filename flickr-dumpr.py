
import json, urllib, os, sys, datetime, time

# Config
USER_ID = u'130608600@N05' # This is the ID for http://www.flickr.com/photos/spacexphotos/
DOWNLOAD_DIR = 'flickr-dumpr'


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

		self.setup()
		albums = self.get_albums()
		albums = self.get_media(albums=albums)
		self.download_manager(albums=albums)

	def setup(self):
		''' API objects '''
		print 'Creating API objects...'
		self.flickrapi_json = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='json')
		self.flickrapi_etree = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='etree')
		self.flickrapi_json.authenticate_via_browser(perms='read')

	def get_albums(self):
		''' Creates an albums dictionary '''
		print 'Getting albums...'
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
		#print response_getSizes_json
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
			page = 1
			photos = []
			videos = []
			items = [] # number of items (photos AND videos)
			print 'Parsing album', album_count, 'of', len(albums), '-', albums[album_id]['title']
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
					
					items.append(m)
					albums[album_id]['media'][media_id] = 	{
																'media_type' : media_type,
																'url_original_format' : url_original_format,
																'dst_filename' : dst_filename
															}				
				page += 1


			album_count += 1
			if len(photos ) > 0:
				print 'Found', len(photos), 'photos'
			if len(videos) > 0:
				print 'Found', len(videos), 'videos'

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


	def create_download_dir(self, path):
		''' Create the download dir unless it already exists '''
		if not os.path.exists(path):
			os.makedirs(path)

	def download_manager(self, albums):
		''' Fetch the albums dictionary with photo/video information, then download each photo into an album folder '''
		for album_id in albums:
			print 'Downloading', albums[album_id]['title'], '...'
			media_counter = 1
			for media_id in albums[album_id]['media']:
				m = albums[album_id]['media'][media_id]
				album_title_validated = self.validate_string( string=albums[album_id]['title'] )
				dst_dir = DOWNLOAD_DIR + '/' + album_title_validated
				self.create_download_dir( path=dst_dir )
				dst_filepath = dst_dir + '/' + m['dst_filename']
				tmp_filepath = dst_dir + '/' + 'flickrdumpr_temp'

				if not os.path.exists(dst_filepath):
					downloaded = False
					while not downloaded:
						time.sleep(1)
						print 'Downloading', media_counter, '/', len(albums[album_id]['media']), '-', m['url_original_format']
						downloaded = self.downloader( url=m['url_original_format'], dst=tmp_filepath )
						if downloaded:
							#print 'Done!'
							os.rename(tmp_filepath, dst_filepath)
						else:
							print 'Error, retrying! (indefinitively)'
				else:
					print 'Skipping', media_counter, '/', len(albums[album_id]['media']), '-', m['url_original_format']

				media_counter += 1


if __name__ == '__main__':
	if check_requirements():
		FlickrDumpr()
