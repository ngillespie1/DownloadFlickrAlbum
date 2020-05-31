#!/usr/bin/env python

import urllib
import sys
import os
import flickrapi
import urllib.request
import time


api_key = u'APIKEY'
api_secret = u'APISECRET'

nArguments = 3
usageString = "usage: python flickr_download.py <user_id> <access_type>"
download_folder = "flickr_downloads"
AlbumId = '72157677674388058'


if len(sys.argv)!= nArguments:
	print(' ' + usageString)	
	sys.exit()
elif not sys.argv[2] == "private" and not sys.argv[2] == "public":
	print("Error: access_type should be either public or private")
	sys.exit()
else:
	user_id = sys.argv[1]
	access_type = sys.argv[2]
		
flickr = flickrapi.FlickrAPI(api_key, api_secret)
if access_type == "private":
	flickr.authenticate_via_browser(perms='read')	

# getting all the albums of the user
setsXML = flickr.photosets.getList(user_id=user_id)

if setsXML.attrib['stat'] == 'ok':
	sets = setsXML.findall('.//photoset')
	print(sets)

	count=1
	try:
		# for each album
		for set in sets:
			id = set.attrib['id']
			if id == '72157705262286295': #or id == '72157705727616844' or id == '72157702039127642' or id == '72157703869229761' or id == '72157705344537314' or id == '72157705766546614':
				
				print("             |")
				print("Downloading \|/ ")
									
				photocount=0
				pagecounter=5
				#Divide number of photos by 500 and Round Up to next 1.
					
				# getting the files in the album             
				while count < pagecounter:
					print(str(count))
					print('Doing Set Number:' + str(count))
					photosXML = flickr.photosets.getPhotos(photoset_id=id, page=count)
					photos = photosXML.findall('.//photo')
					for photo in photos:
						photo_id = photo.attrib['id']
						sizesXML = flickr.photos.getSizes(photo_id=photo_id)
						original_size = sizesXML.find('.//size[@label="Original"]')
						photo_url = original_size.attrib['source']
						photo_name = photo_url.split('/')[-1]
						print ("		" + str(photocount)+ ' - ' + photo_name)	
						if not os.path.exists(download_folder + "/" + id):
							os.makedirs(download_folder + "/" + id)
						urllib.request.urlretrieve(photo_url, download_folder + "/" + id + "/" + photo_name)
						photocount+=1
					count+=1	
					print('Moving on to the Next Set ' + str(count))
					print('')
					
			else:
				print('trying next set')
	except:
		time.sleep(2)
else:
	print("Flickr error")
