#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import feedparser
import json
import requests
import sys
import logging
logging.basicConfig(level=logging.INFO, filename='/var/tmp/rss2json.log', filemode='a', format='%(asctime)s - %(message)s')

def main():
  try:		 
    parser = argparse.ArgumentParser(
      description="Convert file from RSS to JSON. Useful to maintain website \
      sections rendered from JSON files which, in turn, must be \
      dynamically produced from RSS files."
      )
    parser.add_argument("-i", "--input", type=str, required=True, 
      help="Path to RSS file. It can be an absolute URL.")
    parser.add_argument("-o", "--output", type=str, required=True, 
      help="Path to JSON file.")
    args = parser.parse_args()
    rss_file = args.input
    json_file = args.output

    rss_feed = requests.get(rss_file)
    if rss_feed.status_code == requests.codes.ok: 
      json_entries = json.dumps(feedparser.parse(rss_feed.text).entries, ensure_ascii=False)
      with open(json_file, 'w') as f:
        f.write(json_entries)
    else:
      logging.error("Unable to retrieve rss feed")
      sys.exit(1)
  except Exception as e:
      logging.error("Error occured see traceback", exc_info=True)
      sys.exit(1)  

if __name__ == "__main__":
    main()
  
