import datetime
import json
import pathlib
import sys
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
    result = result.replace("\n", " ")
    result = result.replace("\r", " ")
    result = result.replace("\t", " ")
    result = result.replace("\b", " ")
    result = result.replace("\f", " ")
    result = result.replace("<", "＜")
    result = result.replace(">", "＞")
    result = result.replace(":", "：")
    result = result.replace("/", "／")
    result = result.replace("\\", "＼")
    result = result.replace("|", "｜")
    result = result.replace("?", "？")
    result = result.replace("*", "＊")
    result = result.replace("\"", "＂")
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


def safe_int(value):
    try:
        return int(value), True
    except ValueError:
        return 0, False


def main():
    print(sys.argv)
    argv_len = len(sys.argv)
    if argv_len < 2:
        input("Error, Press Enter to exit")
        sys.exit()
    f = open(sys.argv[1], "r", encoding="utf-8")
    data = json.load(f)
    f.close()

    size = len(data)
    print(f"size={len(data)}")

    index_start = 0
    index_end = size - 1

    if argv_len >= 3:
        arg2, is_arg2_valid = safe_int(sys.argv[2])
        if is_arg2_valid and arg2 < size:
            index_start = arg2

    if argv_len >= 4:
        arg3, is_arg3_valid = safe_int(sys.argv[3])
        if is_arg3_valid and index_start <= arg3 < size:
            index_end = arg3

    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    if argv_len > 2 and (index_start != 0 or index_end != size - 1):
        output_folder_name = f"output-{current_time}[{size}][{index_start}-{index_end}]"
    else:
        output_folder_name = f"output-{current_time}[{size}]"

    create_folder(output_folder_name)

    success_count = 0
    fail_count = 0

    sorted_data = sorted(data, key=lambda x: x['created_at'])
    for i in range(index_start, index_end + 1):
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
    print(f"Download task finished! ")
    print(
        f"[{index_start}-{index_end}] total: {index_end - index_start + 1} success: {success_count} fail: {fail_count}")
    input("Press Enter to exit")


if __name__ == '__main__':
    main()

# pyinstaller main.py --onefile