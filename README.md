# Douyin Scraper

# Installation

```
git clone https://github.com/Clemapfel/douyin_scraper.git
```

# Dependencies

```
pip install json
pip install csv
pip install requests
pip install douyin-tiktok-scraper
```

# Usage

### 1. Collect Video URLs

Paste video urls into a file, henceforth assumed to be `douyin_scraper/video_ids.txt`.

Example `video_ids.txt`:
```
https://www.douyin.com/video/7188679476946029885
https://www.douyin.com/video/7188514977211305277
https://www.douyin.com/video/7188463948864261434
```
### 2. Specify Metadata Filter

Paste json keys into a file, henceforth assumed to be `douying_scraper/filter.txt`. Data for these keys will be extracted 
from the raw metadata into the output csv file.

Example `filter.txt`:
```
digg_count
play_count
share_count
```

For a full list of allowed keys, run the script once and inspect one of the `raw.json` files in `douyin_scraper/out`.

### 3. Execute Script

In your console, navigate to `douyin_scraper/`, then execute:

```commandline
python3 scrape.py video_ids.txt filter.txt 
```

Where `video_ids.txt` is the file from step 1, `filter.txt` the file from step 2, both of which are located in the folder same folder as `scrape.py`.

Let the script run until the following appear:
```
Process finished with exit code 0
```

### 4. Collect Output

For each script run, a new folder in `./out` will be created, each containing the videos and video metadata for all videos
in `video_ids.txt`. Furthermore, an a `.csv` with the current time in the format `YYYY-MM-DD_hh:mm` in its name that contains
the values for all keys specified by `filter.txt` will appear in the same directory as the script.