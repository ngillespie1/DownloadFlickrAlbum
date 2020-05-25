#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 08:28:59 2020

Use: python DownloadFlickrAlbum(s) <FlickrUserID> <public>
"""



#!/usr/bin/env python

import urllib
import sys
import os
import flickrapi
import xml.etree.ElementTree as ET
import urllib.request


api_key = u'INSERT HERE'
api_secret = u'INSERT HERE'

nArguments = 3
usageString = "usage: python flickr_download.py <user_id> <access_type>"
download_folder = "flickr_downloads"

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

	# for each album
	for set in sets:
		id = set.attrib['id']
		print(set)
		print(id)
        # Insert Flickr Albums Here
		if id == "72157677674388058" or id == "72157705727616844" or id == '72157702039127642':
			
			print("             |")
			print("Downloading \|/ ")
		#print set.find('title').text
			print

		
			if not os.path.exists(download_folder + "/" + id):
				os.makedirs(download_folder + "/" + id)
		
#		# store the metadata of the album in a file
#		metadata_file = open(download_folder + "/" + id + "/" + id + '.xml','w')
#		metadata_file.write(ET.tostring(set, encoding='utf8', method='xml'))
#		metadata_file.close()

		# getting the files in the album
			photosXML = flickr.photosets.getPhotos(photoset_id=id)
			photos = photosXML.findall('.//photo')

		# for each file in the album
			for photo in photos:
				photo_id = photo.attrib['id']
			
				sizesXML = flickr.photos.getSizes(photo_id=photo_id)
				original_size = sizesXML.find('.//size[@label="Original"]')

				photo_url = original_size.attrib['source']

				photo_name = photo_url.split('/')[-1]
				print ("		" + photo_name)
			
			# store the metadata of the file
#			metadata_file = open(download_folder + "/" + id + "/" + photo_name.split('.')[-2] + '.xml','w')
#			metadata_file.write(ET.tostring(photo, encoding='utf8', method='xml'))
#			metadata_file.close()

			# downloading the file
		#if id == "72157677674388058":
				urllib.request.urlretrieve(photo_url, download_folder + "/" + id + "/" + photo_name)
		else:
			print('trying next set')
else:
	print("Flickr error")