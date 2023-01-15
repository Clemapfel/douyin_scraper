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

async def video_url_to_video_id(url: str) -> str:
    """
    convert video url to douyin id

    :param url: link to video in the form https://www.douyin.com/video/<video id>
    :return: video id
    """
    return await scraper.get_douyin_video_id(url)

async def get_video_download_link(id: str) -> str:
    """
    get direct download link for video

    :param id: video id obtained by video_url_to_video_id
    :return: direct download link
    """

    # super hacky, the download interface doesn't seem to be exposed so if this link ever changes
    # this will break. Is there maybe a resource link somewhere in video data?

    download_url_left = "https://api.douyin.wtf/download?url=https%3A%2F%2Fwww.douyin.com%2Fvideo%2F"
    download_url_right = "&prefix=true&watermark=false"
    return download_url_left + id + download_url_right

def warn_if_target_dir_is_file(dir) -> None:
    """
    print a warning if a file of specified name already exists

    :param dir: full uri
    :return: nothing
    """
    if os.path.isfile(dir):
        print("[ERROR] File " + os.curdir() + dir + " already exists. Please delete/move it and rerun this script.")
        exit(1)

video_urls = [] # list of video urls
json_keys = []  # list of keys, see raw.json for a full list of possible keys
async def update_video_data():
    """
    take video ids from file at argv[1] and download them and their metadata into ./out
    """

    # create output directory structure
    out_dir = "./out"
    warn_if_target_dir_is_file(out_dir)

    if not os.path.isdir(out_dir):
        os.mkdir("./out")

    for video_url in video_urls:

        video_id = await video_url_to_video_id(video_url)
        video_dir = out_dir + "/" + video_id

        warn_if_target_dir_is_file(video_dir)
        if not os.path.isdir(video_dir):
            os.mkdir(video_dir)

        metadata_download_success = False
        json_raw_path = video_dir + "/raw.json"
        try:
            metadata = await download_video_data(video_url)
            metadata["request_timestamp"] = datetime.timestamp(datetime.now())
            json_raw_file = open(json_raw_path, "w")
            json_raw_file.write(json.dumps(metadata))
            json_raw_file.close()
            metadata_download_success = True
        except:
            metadata_download_success = False

        if metadata_download_success:
            print("[LOG] Wrote metadata to " + os.path.abspath(json_raw_path))
        else:
            print("[ERROR] Unable to download metadata for video at " + video_url)

        video_path = video_dir + "/video.mp4"

        if not os.path.isfile(video_path): # prevent redownloading if video already exists, metadata is updated though
            download_link = await get_video_download_link(video_id)
            video_download_success = False
            try:
                req = requests.get(download_link, allow_redirects=True)
                open(video_path, 'wb').write(req.content)
                video_download_success = True
            except:
                video_download_success = False

            if video_download_success:
                print("[LOG] Wrote video to " + os.path.abspath(video_path))
            else:
                print("[ERROR] Unable to download video file for video at " + video_url)
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
    n_videos = 0

    csv_file = open("./out.csv", "w")
    csv_writer = csv.DictWriter(csv_file, [])
    csv_writer_initialized = False

    for each in os.listdir("./out"):

        video_id = each
        path = os.path.join("./out", each)
        if not os.path.isdir(path):
            continue

        # extract values from json dict, recursive since some items are dicts themself
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
        items["video_id"] = video_id
        items["local_uri"] = os.path.abspath(path)
        items["time_accessed"] = timestamp.strftime("%d.%m.%Y %H:%M:%S")
        extract_keys_recursively(metadata, items)

        if not csv_writer_initialized:
            csv_writer = csv.DictWriter(csv_file, items.keys())
            csv_writer.writeheader()
            csv_writer_initialized = True

        csv_writer.writerow(items)
        n_videos += 1

    csv_file.close()
    print("[LOG] Wrote csv output for session to " + os.path.abspath(out_dir + "/out.csv"))
    print("[LOG] " + str(n_videos) + " videos processed")
    print("done.")

### MAIN ##################################################################################

# load video urls and filter from argv[1] and argv[2] respectively
if len(sys.argv) != 3:
    print("[ERROR] Wrong number of arguments. Usage: `python3 scrape.py <video ids file>.txt <metadata keys file>.txt")
    exit(1)

for line in open(sys.argv[1]).readlines():
    video_urls.append(line.split("\n")[0])

for line in open(sys.argv[2]).readlines():
    json_keys.append(line.split("\n")[0])

if len(json_keys) == 0:
    print("[ERROR] Metadata key file at " + os.path.abspath(sys.argv[2]) + " contains no keys. Exiting...")
    exit(1)

# update ./out folder with metadata and video files
asyncio.run(update_video_data())

# run through ./out and collect filtered as .csv
update_csv()
