import os
import sys
import shutil
import logging
import scraper
import argparse
import subprocess
from sys import argv

# disown() taken from https://github.com/dylanaraps/pywal/blob/master/pywal/util.py
def disown(cmd):
	"""Call a system command in the background,
	   disown it and hide it's output."""
	subprocess.Popen(cmd,
					 stdout=subprocess.DEVNULL,
					 stderr=subprocess.DEVNULL)

# xconf() taken from https://github.com/dylanaraps/pywal/blob/master/pywal/wallpaper.py
def xfconf(path, img):
	"""Call xfconf to set the wallpaper on XFCE."""
	disown(["xfconf-query", "--channel", "xfce4-desktop",
				 "--property", path, "--set", img])

# set_wm_wallpaper() taken from https://github.com/dylanaraps/pywal/blob/master/pywal/wallpaper.py
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


# get_desktop_env() taken from https://github.com/dylanaraps/pywal/blob/master/pywal/wallpaper.py
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

# set_desktop_wallpaper() taken from https://github.com/dylanaraps/pywal/blob/master/pywal/wallpaper.py
def set_desktop_wallpaper(desktop, img):
	"""Set the wallpaper for the desktop environment."""
	desktop = str(desktop).lower()

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
		disown(["gsettings", "set",
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
	
	args = parser.parse_args()
	query = args.search
	wallpaper_dir = "wallpapers"

	if not os.path.exists(wallpaper_dir):
		os.makedirs(wallpaper_dir)

	# Get filename created from scraper based on query
	filename = scraper.scrape(query, wallpaper_dir)
	# Get desktop environment if it exists
	desktop = get_desktop_env()
	# Set wallpaper to scraped image
	this_dir = os.getcwd()
	img_path = os.path.join(this_dir, wallpaper_dir, filename)
	print(img_path)
	set_desktop_wallpaper(desktop, img_path)
