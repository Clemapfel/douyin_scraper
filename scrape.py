import json
import asyncio
import sys
import os
import csv
import requests
from datetime import datetime
from douyin_tiktok_scraper.scraper import Scraper

scraper = Scraper()
async def download_video_data(url: str) -> dict:
    """
    download video metadata

    :param url: link to video in the form https://www.douyin.com/video/<video id>
    :return: dictionary with metadata
    """
    return await scraper.hybrid_parsing(video_url=url)

async def get_video_download_link(id: str) -> str:
    """
    get direct download link for video

    :param url: link to video in the form https://www.douyin.com/video/<video id>
    :return: dictionary with metadata
    """

    # super hacky, the download interface doesn't seem to be exposed so if this link ever changes
    # this will break. Is there maybe a resource link somewhere in video data?

    download_url_left = "https://api.douyin.wtf/download?url=https%3A%2F%2Fwww.douyin.com%2Fvideo%2F"
    download_url_right = "&prefix=true&watermark=false"
    return download_url_left + id + download_url_right

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

async def update_video_data():
    """
    take video ids from argv[1] and download them and their metadata into ./out
    """

    # create output directory structure
    out_dir = "./out"
    warn_if_target_dir_is_file(out_dir)

    if not os.path.isdir(out_dir):
        os.mkdir("./out")

    # metadata and video into ./out
    for video_url in video_urls:

        video_id = await video_url_to_video_id(video_url)
        video_dir = out_dir + "/" + video_id

        print("\n[LOG] Downloading video data for video " + video_id + "...")

        warn_if_target_dir_is_file(video_dir)
        if not os.path.isdir(video_dir):
            os.mkdir(video_dir)

        json_raw_path = video_dir + "/raw.json"
        metadata = await download_video_data(video_url)
        metadata["request_timestamp"] = datetime.timestamp(datetime.now())
        json_raw_file = open(json_raw_path, "w")
        json_raw_file.write(json.dumps(metadata))
        json_raw_file.close()
        print("[LOG] Wrote metadata to " + os.path.abspath(json_raw_path))

        video_path = video_dir + "/video.mp4"

        if not os.path.isfile(video_path):
            download_link = await get_video_download_link(video_id)
            req = requests.get(download_link, allow_redirects=True)
            open(video_path, 'wb').write(req.content)
            print("[LOG] Wrote video to" + os.path.abspath(video_path))
        else:
            print("[LOG] Video already downloaded, skipping this entry...")

        print("\n")

def update_csv():
    """
    parse ./out raw json files and assemble filtered csv
    """

    out_dir = "./out"
    warn_if_target_dir_is_file(out_dir)

    if not os.path.isdir(out_dir):
        os.mkdir("./out")

    timestamp = datetime.fromtimestamp(datetime.timestamp(datetime.now()))

    video_dicts = []
    csv_file = open("./out.csv", "w")
    csv_writer = csv.DictWriter(csv_file, [])
    csv_writer_initialized = False

    for each in os.listdir("./out"):

        path = os.path.join("./out", each)
        if not os.path.isdir(path):
            continue

        # extract values
        def extract_keys_recursively(dict_in, items):
            for item in dict_in.items():
                if isinstance(item[1], dict):
                    extract_keys_recursively(item[1], items)
                elif item[0] in json_keys:
                    items[item[0]] = item[1]

        json_path = path + "/raw.json"
        file = open(json_path, "r")
        metadata = json.load(file)
        items = dict()
        items["video_id"] = path
        items["local_uri"] = os.path.abspath(path)
        items["time_accessed"] = timestamp.strftime("%d.%m.%Y %H:%M:%S")
        extract_keys_recursively(metadata, items)

        if not csv_writer_initialized:
            csv_writer = csv.DictWriter(csv_file, items.keys())
            csv_writer.writeheader()
            csv_writer_initialized = True

        csv_writer.writerow(items)

    csv_file.close()
    print("[LOG] Wrote csv output for session to " + os.path.abspath(out_dir + "/out.csv"))
    print("done.")

# main
asyncio.run(update_video_data())
update_csv()










