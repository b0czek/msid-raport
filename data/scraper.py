import requests
from datetime import datetime
import json 
import logging
import argparse
import os

API_URL = "https://www.olx.pl/api/v1/offers"

PAGE_LIMIT = 50

CATEGORY_ID = 15 # mieszkania na wynajem
REGION_ID = 3 # woj. dolnośląskie
CITY_ID = 19701 # Wrocław

def parse_arguments():
    parser = argparse.ArgumentParser(description="Script for scraping olx offers")
    parser.add_argument("--output-dir", default=os.path.curdir, help="Output directory where scrapped data will be saved, current directory by default")
    
    return parser.parse_args()


def fetch_page(offset):
    logging.log(logging.DEBUG, f"fetching page {(offset / PAGE_LIMIT) + 1}")
    params = {
        "category_id": CATEGORY_ID,
        "region_id": REGION_ID,
        "city_id": CITY_ID,
        "limit": PAGE_LIMIT,
        "offset": offset,
        "sort_by": "created_at:desc"
    }


    response = requests.get(API_URL, params=params)
    response.raise_for_status()

    return response.json()
    print(isinstance(response.json(), dict))

def main(args):
    args = parse_arguments()


    try:
        base_page = fetch_page(0)
    except:
        print("Failed to scrape offers.")
        exit(1)

    # try to get total number of available offers
    try:
        available_offers = base_page['metadata']['total_elements']
    except:
        print("Could not get numbers of available offers.")
        exit(1)

    output = base_page['data']

    failed_any = False

    offset = PAGE_LIMIT
    while offset <= available_offers:
        try:
            page = fetch_page(offset)
        except:
            failed_any = True
            print(f"Failed to fetch page {(offset / PAGE_LIMIT) + 1}.")

        output = output + page['data']
        offset += PAGE_LIMIT
    time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = time + ("-partial"if failed_any else "") + ".json"

    with open(os.path.join(args.output_dir, filename), "w") as f:
        f.write(json.dumps(output))

if __name__ == "__main__":
    main()