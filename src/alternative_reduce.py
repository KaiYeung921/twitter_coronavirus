#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_folder', default='outputs')
parser.add_argument('--output_path', required=True)
parser.add_argument('--hashtags', nargs='+', required=True)
args = parser.parse_args()

import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re
import datetime
from collections import defaultdict

# construct dataset: {hashtag: {date_object: total_count}}
dataset = defaultdict(lambda: defaultdict(int)) 
all_dates = set() # Keep track of all dates we encounter

for filename in os.listdir(args.input_folder):
    if filename.endswith('.lang'):
        with open(os.path.join(args.input_folder, filename)) as f:
            daily = json.load(f)
        
        match = re.search(r'geoTwitter(\d{2})-(\d{2})-(\d{2})', filename)
        if match:
            year_str, month_str, day_str = match.groups()
            year = 2000 + int(year_str) 
            month = int(month_str)
            day = int(day_str)
            
            dt = datetime.date(year, month, day)
            all_dates.add(dt)
            
            for hashtag in args.hashtags:
                if hashtag in daily:
                    total_for_day = sum(daily[hashtag].values())
                    dataset[hashtag][dt] += total_for_day

if not all_dates:
    print("No valid data found in the input folder.")
    exit(1)

start_date = min(all_dates)
end_date = max(all_dates)
date_range = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]

fig, ax = plt.subplots(figsize=(10, 6))

for hashtag in args.hashtags:
    y = [dataset[hashtag].get(date, 0) for date in date_range]
    ax.plot(date_range, y, label=hashtag)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b')) # '%b' gives Jan, Feb, Mar, etc.

plt.xlabel('Month of the year')
plt.ylabel('Number of tweets')
plt.title('Tweet counts over time')
plt.legend()
plt.tight_layout()

plt.savefig(args.output_path)
print(f'Saved plot to {args.output_path}')
