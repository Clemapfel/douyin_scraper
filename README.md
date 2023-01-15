# Douyin Scraper

# Dependencies

```
pip install douyin-tiktok-scraper
```

# Usage

# 1. Collect Video URLs

Paste video urls into a file, henceforth assumed to be `douyin_scraper/video_ids.txt`.

Example:
```
https://www.douyin.com/video/7188679476946029885
https://www.douyin.com/video/7188514977211305277
https://www.douyin.com/video/7188463948864261434
```
# 2. Specify Metadata Filter

Past json keys into a file, henceforth assumed to be `douying_scraper/keys.txt`.

Example:
```
digg_count
play_count
share_count
create_time
aweme_id
```

# 3. Execute Script

In your console, navigate to `douyin_scraper/`, then execute:

```commandline
python3 scrape.py video_ids.txt keys.txt 
```

Where `video_ids.txt` is the file from step 1, `keys.txt` the file from step 2.


Let the script run until the following appear:
```
Wrote csv output for session to /home/clem/Workspace/douyin_scraper/out/out.csv
done.

Process finished with exit code 0
```

# 4. Access Data

You can find the raw video data and json in `douyin_scraper/out/<video id>`.
The final .csv file will be in `douyin_scraper/out/out_<timestamp>.csv`.