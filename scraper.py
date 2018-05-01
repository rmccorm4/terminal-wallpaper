from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import os
import argparse
import sys
import json
import random

# adapted from http://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search

def get_soup(url,header):
	return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')

'''
def scrape(args):
	parser = argparse.ArgumentParser(description='Scrape Google images')
	parser.add_argument('-s', '--search', default='desktop background 1080p', type=str, help='search term')
	parser.add_argument('-n', '--num_images', default=1, type=int, help='num images to save')
	parser.add_argument('-d', '--directory', default=os.path.join(os.environ['HOME'], 'Downloads'), type=str, help='save directory')
	args = parser.parse_args()
	query = args.search
	max_images = args.num_images
	save_directory = args.directory
'''

def scrape(query, save_directory):

	image_type="Action"
	
	search_term = query[:]
	# Clean up query
	if query != 'desktop background 1080p':
		# If a search term specific like 'Space' or 'Cats', append
		# desktop background description to the query for wallpapers
		query += ' desktop background 1080p' 
	else:
		search_term = 'random'

	query= query.split()
	query='+'.join(query)
	url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	soup = get_soup(url,header)
	ActualImages=[]# contains the link for Large original images, type of  image
	for a in soup.find_all("div",{"class":"rg_meta"}):
		link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
		ActualImages.append((link,Type))
	
	# Get random image from search results so its different every time
	# Only looking at first 30 for best results with some diversity still
	rand_image_num = random.randint(0, 30)
	#for i , (img , Type) in enumerate( ActualImages[0:max_images]):
	# Kept as this syntax so I didn't have to change any code, ignore the loop
	# despite it being for a single image
	for i , (img , Type) in enumerate( ActualImages[rand_image_num:rand_image_num+1]):
		try:
			req = urllib.request.Request(img, headers=header)
			raw_img = urllib.request.urlopen(req).read()
			if len(Type)==0:
				retval = "img_" + search_term +".jpg"
				f = open(os.path.join(save_directory, retval), 'wb')
			else :
				retval = "img_" + search_term +"."+Type
				f = open(os.path.join(save_directory, retval), 'wb')
			f.write(raw_img)
			f.close()
		except Exception as e:
			print("could not load : " + img)
			print(e)
	
	# Return filename created
	return retval

if __name__ == '__main__':
	from sys import argv
	try:
		scrape(argv)
	except KeyboardInterrupt:
		pass
	sys.exit()
