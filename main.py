#!/usr/bin/env python3
# Created by sc1341
#
# This tool is intended to locate links to other directories and sites
# throughout the webpage to make enumeration of a site easier and faster
# 
#
import argparse
import random
import requests
import os

from bs4 import BeautifulSoup

from useragents import useragents


class WebCrawler:

	def __init__(self, url, filename):
		if url.startswith("http://") or url.startswith("https://"):
			self.url = url
		else:
			self.url = "http://" + url
		self.filename = filename

	def scrape_site(self):
		"""
		Scrapes the site and prints out the results to the user,
		it also creates a file with the directories found on the site
		"""
		try:
			r = requests.get(self.url, headers={"User-Agent": random.choice(useragents)})
		except ConnectionError:
			print("Error! URL Invalid")


		soup = BeautifulSoup(r.text, 'html.parser')
		directories = soup.find_all('a')
		if not os.path.exists(self.filename):
			with open(self.filename, "w") as f:
				for value in directories:
					try:
						print(value.attrs["href"])
						f.write(value.attrs["href"] + "\n")
					except ValueError:
						print("Error parsing <a> tag href content")
		else:
			print("File name error! Please rename your file to something that does not exist")



def parse_args():
    parser = argparse.ArgumentParser(description="Web Directory Crawler")
    parser.add_argument("--url", help="Webpage url", required=True, nargs=1)
    parser.add_argument("--filename", help="Output file name", required=True, nargs=1)
    return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	w = WebCrawler(args.url[0], args.filename[0])
	w.scrape_site()

