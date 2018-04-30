if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Scrape Google images')
	parser.add_argument('-s', '--search', default='desktop background 1080p', type=str, help='search term')
	parser.add_argument('-n', '--num_images', default=1, type=int, help='num images to save')
	parser.add_argument('-d', '--directory', default=os.path.join(os.environ['HOME'], 'Downloads'), type=str, help='save directory')

