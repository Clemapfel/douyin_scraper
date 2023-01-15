# Douyin Scraper

# Installation

```
git clone https://github.com/Clemapfel/douyin_scraper.git
```

# Dependencies

```
pip install requests
pip install douyin-tiktok-scraper
```

# Usage

### 1. Collect Video URLs

Paste video urls into a file, henceforth assumed to be `douyin_scraper/video_ids.txt`.

Example:
```
https://www.douyin.com/video/7188679476946029885
https://www.douyin.com/video/7188514977211305277
https://www.douyin.com/video/7188463948864261434
```
### 2. Specify Metadata Filter

Paste json keys into a file, henceforth assumed to be `douying_scraper/filter.txt`. Data for these keys will be extracted 
from the raw metadata into the output csv file.

Example:
```
digg_count
play_count
share_count
```

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

A filtered .csv will have appeared as `douyin_scraper/out.csv`. Furthermore, the folder `douyin_scraper/out` will have 
been created, it contains the raw metadata and video files. Do not modify this folder, as it may mess up the script.

One column in `out.csv` is named `local_uri`. This column contains a link to the downloaded video file on your local 
machine. 