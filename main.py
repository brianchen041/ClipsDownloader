import datetime
import json
import pathlib
import random
import sys
import time
import urllib.request


# parse time and change to local timezone
# https://stackoverflow.com/a/63988322/10217112
def parse_time(time_str):
    dt = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%Y-%m-%d %H-%M-%S")


# ＜＞：／＼｜？＊
# https://stackoverflow.com/a/31976060/10217112
def filter_title(title_str):
    result = title_str
    result = result.replace("<", "＜")
    result = result.replace(">", "＞")
    result = result.replace(":", "：")
    result = result.replace("/", "／")
    result = result.replace("\\", "＼")
    result = result.replace("|", "｜")
    result = result.replace("?", "？")
    result = result.replace("*", "＊")
    return result


# https://stackoverflow.com/a/22776/10217112
def download_file(url, file_name):
    try:
        urllib.request.urlretrieve(url, file_name)
        return True, None
    except Exception as e:
        return False, e


def create_folder(name):
    pathlib.Path(name).mkdir(exist_ok=True)
    print(f"Create folder: {name}")


def is_exist(name):
    return pathlib.Path(name).exists()


def main():
    print(sys.argv)
    if len(sys.argv) != 2:
        input("Error, Press Enter to exit")
        sys.exit()
    f = open(sys.argv[1], "r", encoding="utf-8")
    data = json.load(f)
    f.close()

    size = len(data)
    print(f"size={len(data)}")

    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    output_folder_name = f"output-{current_time}-{size}"

    create_folder(output_folder_name)

    success_count = 0
    fail_count = 0

    sorted_data = sorted(data, key=lambda x: x['created_at'])
    for i in range(size):
        title = filter_title(sorted_data[i]["title"])
        create_time = parse_time(sorted_data[i]["created_at"])
        download_url = sorted_data[i]["download_url"]
        clip_id = sorted_data[i]["id"]

        file_name = f"{create_time} {title}.mp4"
        if is_exist(f"{output_folder_name}/{file_name}"):
            print(f"Filename collision {clip_id}")
            file_name = f"{create_time}_{title}_{clip_id[-7:]}.mp4"  # Add some id, to prevent filename collision

        success, error = download_file(download_url, f"{output_folder_name}/{file_name}")
        if success:
            print(f"{i} download successful: {file_name}")
            success_count += 1
        else:
            print(f"{i} download failed: {file_name}")
            print(error)
            fail_count += 1
    print(f"Download task finished! total: {size} success: {success_count} fail: {fail_count}")
    input("Press Enter to exit")


if __name__ == '__main__':
    main()

# pyinstaller main.py --onefile