import json
import asyncio
import sys
import os
import csv
from datetime import datetime

from douyin_tiktok_scraper.scraper import Scraper

scraper = Scraper()
async def download_metadata(url: str) -> dict:
    """
    download video metadata

    :param url: link to video in the form https://www.douyin.com/video/<video id>
    :return: dictionary with metadata
    """
    return await scraper.hybrid_parsing(video_url=url)

async def download_video(id):
    """
    download video file

    :param url: link to video in the form https://www.douyin.com/video/<video id>
    :return:
    """
    print("todo")

async def video_url_to_video_id(url: str) -> str:
    """
    convert video url to douyin id

    :param url: link to video in the form https://www.douyin.com/video/<video id>
    :return: video id
    """
    return await scraper.get_douyin_video_id(url)

def warn_if_target_dir_is_file(dir):
    """
    print a warning if a file of specified name already exists

    :param dir: full uri
    :return: nothing
    """
    if os.path.isfile(dir):
        print("[ERROR] File " + os.curdir() + dir + " already exists. Please delete/move it and rerun this script.")


# load video url batch form sys argument #1
video_urls = []
for line in open(sys.argv[1]).readlines():
    video_urls.append(line.split("\n")[0])

# load json key list from sys argument #2
json_keys = []
for line in open(sys.argv[2]).readlines():
    json_keys.append(line.split("\n")[0])
async def main():

    timestamp = datetime.fromtimestamp(datetime.timestamp(datetime.now()))

    # create output directory structure
    out_dir = "./out"
    warn_if_target_dir_is_file(out_dir)

    print("Initializing session output at " + os.path.abspath(out_dir))

    if not os.path.isdir(out_dir):
        os.mkdir("./out")

    video_dicts = []

    csv_file = open(out_dir + "/out_" + timestamp.strftime("%d_%m_%Y_%H_%M_%S") + ".csv", "w")
    csv_writer = csv.DictWriter(csv_file, [])
    csv_writer_initialized = False

    # download and format metadata
    for video_url in video_urls:

        video_id = await video_url_to_video_id(video_url)
        video_dir = out_dir + "/" + video_id

        warn_if_target_dir_is_file(video_dir)
        if not os.path.isdir(video_dir):
            os.mkdir(video_dir)

        metadata = await download_metadata(video_url)
        metadata["request_timestamp"] = datetime.timestamp(datetime.now())
        json_raw_file = open(video_dir + "/raw.json", "w")
        json_raw_file.write(json.dumps(metadata))
        json_raw_file.close()

        # extract values
        def extract_keys_recursively(dict_in, items):
            for item in dict_in.items():
                if isinstance(item[1], dict):
                    extract_keys_recursively(item[1], items)
                elif item[0] in json_keys:
                    items[item[0]] = item[1]

        items = dict()
        items["video_id"] = video_id
        items["local_uri"] = os.path.abspath(video_dir)
        items["time_accessed"] = timestamp.strftime("%d.%m.%Y %H:%M:%S")
        extract_keys_recursively(metadata, items)

        if not csv_writer_initialized:
            csv_writer = csv.DictWriter(csv_file, items.keys())
            csv_writer.writeheader()
            csv_writer_initialized = True

        csv_writer.writerow(items)
        print("\nWrote video data to " + items["local_uri"] + "\n")

    csv_file.close()
    print("Wrote csv output for session to " + os.path.abspath(out_dir + "/out.csv"))
    print("done.")

asyncio.run(main())





