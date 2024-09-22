import argparse 
import requests
import csv 
import re 
from collections import Counter 
import urllib.request 

def downloadData(url):
    with urllib.request.urlopen(url) as response: 
        response = response.read().decode('utf-8')
    return response

def process_log_data(log_data):
    image_count = 0 
    total_requests = 0 
    browser_counter = Counter()
    
    image_pattern = re.compile(r'\.(jpg|gif|png)$')
    browser_pattern = re.compile(r'Firefox|Chrome|MSIE|Safari')

    reader = csv.reader(log_data.splitlines())
    for line in reader:
        if len(line) < 5:
            continue 
        path, datetime_accessed, user_agent, status, request_size = line 

        total_requests += 1

        if image_pattern.search(path): 
            image_count += 1
        
        browser_match = browser_pattern.search(user_agent)
        if browser_match:
            browser_counter[browser_match.group()] += 1
    return total_requests, image_count, browser_counter

def calculate_image_percentage(total_requests, image_count):
    if total_requests == 0:
        return 0.0
    return (image_count / total_requests) * 100

def most_popular_browser(browser_counter):
    if not browser_counter:
        return None 
    return browser_counter.most_common(1)[0]

def main(url):
    print(f"Running main with URL = {url}...")
    log_data = downloadData(url)
    total_requests, image_count, browser_counter = process_log_data(log_data)
    image_percentage = calculate_image_percentage(total_requests, image_count)
    print(f"Image requests account for {image_percentage:.1f}% of sll requests.")

    popular_browser = most_popular_browser(browser_counter)
    if popular_browser:
        browser_name, count = popular_browser 
        print(f"The most popular browser is {browser_name} with {count} requests.")
    else: 
        print("No browser data available.")
    
    if __name__ == "__main__":
        parser = argparse.Argumentparser()
        parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
        args = parser.parse_args()
        main(args.url)
