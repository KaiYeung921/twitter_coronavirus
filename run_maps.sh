#!/bin/bash

# Loop over each file in the dataset
for file in /data/Twitter\ dataset/geoTwitter20-*.zip; do
  # Run the map.py command on the file
  nohup python3 src/map.py --input_path="$file" --output_folder="outputs" &
done

