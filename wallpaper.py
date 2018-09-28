import os
import sys
import shutil
import random
import logging
import scraper
import platform
import argparse
import subprocess
from sys import argv

'''
Most of these functions were taken/slightly modified from 'Pywal' by Dylanaraps,
some of my own touches added here and there, but its not much.
'''

# Taken from https://github.com/dylanaraps/pywal/blob/master/pywal/util.py
def disown(cmd):
	"""Call a system command in the background,
	   disown it and hide it's output."""
	subprocess.Popen(cmd,
					 stdout=subprocess.DEVNULL,
					 stderr=subprocess.DEVNULL)

# Taken from https://github.com/dylanaraps/pywal/blob/master/pywal/wallpaper.py
def xfconf(path, img):
	"""Call xfconf to set the wallpaper on XFCE."""
	disown(["xfconf-query", "--channel", "xfce4-desktop",
				 "--property", path, "--set", img])

# Taken from https://github.com/dylanaraps/pywal/blob/master/pywal/wallpaper.py
def set_mac_wallpaper(img):
	"""Set the wallpaper on macOS."""
	HOME = os.getenv("HOME", os.getenv("USERPROFILE"))
	db_file = "Library/Application Support/Dock/desktoppicture.db"
	db_path = os.path.join(HOME, db_file)
	subprocess.call(["sqlite3", db_path, "update data set value = '%s'" % img])

	# Kill the dock to fix issues with cached wallpapers.
	# macOS caches wallpapers and if a wallpaper is set that shares
	# the filename with a cached wallpaper, the cached wallpaper is
	# used instead.
	subprocess.call(["killall", "Dock"])

# Taken from https://github.com/dylanaraps/pywal/blob/master/pywal/wallpaper.py
def set_win_wallpaper(img):
	"""Set the wallpaper on Windows."""
	# There's a different command depending on the architecture
	# of Windows. We check the PROGRAMFILES envar since using
	# platform is unreliable.
	if "x86" in os.environ["PROGRAMFILES"]:
		ctypes.windll.user32.SystemParametersInfoW(20, 0, img, 3)
	else:
		ctypes.windll.user32.SystemParametersInfoA(20, 0, img, 3)

# Taken from https://github.com/dylanaraps/pywal/blob/master/pywal/wallpaper.py
def set_wm_wallpaper(img):
	"""Set the wallpaper for non desktop environments."""
	if shutil.which("feh"):
		disown(["feh", "--bg-fill", img])

	elif shutil.which("nitrogen"):
		disown(["nitrogen", "--set-zoom-fill", img])

	elif shutil.which("bgs"):
		disown(["bgs", "-z", img])

	elif shutil.which("hsetroot"):
		disown(["hsetroot", "-fill", img])

	elif shutil.which("habak"):
		disown(["habak", "-mS", img])

	elif shutil.which("display"):
		disown(["display", "-backdrop", "-window", "root", img])

	else:
		logging.error("No wallpaper setter found.")
		return


# Taken from https://github.com/dylanaraps/pywal/blob/master/pywal/wallpaper.py
def get_desktop_env():
	"""Identify the current running desktop environment."""
	desktop = os.environ.get("XDG_CURRENT_DESKTOP")
	if desktop:
		return desktop

	desktop = os.environ.get("DESKTOP_SESSION")
	if desktop:
		return desktop

	desktop = os.environ.get("GNOME_DESKTOP_SESSION_ID")
	if desktop:
		return "GNOME"

	desktop = os.environ.get("MATE_DESKTOP_SESSION_ID")
	if desktop:
		return "MATE"

	desktop = os.environ.get("SWAYSOCK")
	if desktop:
		return "SWAY"

	return None

# Taken from https://github.com/dylanaraps/pywal/blob/master/pywal/wallpaper.py
def set_desktop_wallpaper(desktop, img):
	"""Set the wallpaper for the desktop environment."""
	desktop = str(desktop).lower()
	print('Desktop Environment:', desktop)

	if "xfce" in desktop or "xubuntu" in desktop:
		# XFCE requires two commands since they differ between versions.
		xfconf("/backdrop/screen0/monitor0/image-path", img)
		xfconf("/backdrop/screen0/monitor0/workspace0/last-image", img)

	elif "muffin" in desktop or "cinnamon" in desktop:
		disown(["gsettings", "set",
					 "org.cinnamon.desktop.background",
					 "picture-uri", "file://" + img])
					 #"picture-uri", "file://" + urllib.parse.quote(img)])

	elif "gnome" in desktop:
		disown(["/usr/bin/gsettings", "set",
					 "org.gnome.desktop.background",
					 "picture-uri", "file://" + img])
					 #"picture-uri", "file://" + urllib.parse.quote(img)])

	elif "mate" in desktop:
		disown(["gsettings", "set", "org.mate.background",
					 "picture-filename", img])

	elif "sway" in desktop:
		disown(["swaymsg", "output", "*", "bg", img, "fill"])

	else:
		set_wm_wallpaper(img)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Scrape Google images')
	parser.add_argument('-s', '--search', default='desktop background 1080p', type=str, help='search term')
	parser.add_argument('-n', '--number', default=random.randint(0, 30), type=int, help='n-th result to choose as background')
	parser.add_argument('-f', '--fun', action='store_true', help='option to remove the "desktop background 1080p" from search term for more specific results but less quality')
	parser.add_argument('-i', '--image', default='', type=str, help='image to set your wallpaper as')
	
	args = parser.parse_args()
	query = args.search
	result = args.number
	fun = args.fun
	image = args.image
	wallpaper_dir = "wallpapers"

	if not os.path.exists(wallpaper_dir):
		os.makedirs(wallpaper_dir)

	if image == '':
		print('Scraping a Desktop Background from Google Images...')
		# Get filename created from scraper based on query
		filename = scraper.scrape(query, wallpaper_dir, result, fun)
		# Set wallpaper to scraped image
		img_path = os.path.join(os.getcwd(), wallpaper_dir, filename)
		print('Desktop Background saved to:', img_path)
	# If image already specified
	else:
		filename = image
		img_path = os.path.join(os.getcwd(), filename)
		print('Using image already saved in:', img_path)

	# Get operating system name from system
	operating_system = platform.uname()[0]
	print('Operating System:', operating_system)

	if operating_system == 'Darwin':
		set_mac_wallpaper(img_path)

	elif operating_system == 'Windows':
		set_win_wallpaper(img_path)

	else:
		# Get desktop environment if it exists
		desktop = get_desktop_env()
		set_desktop_wallpaper(desktop, img_path)
