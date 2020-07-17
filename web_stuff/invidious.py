import urllib.request
import datetime
import json
import mpv

player = mpv.MPV(ytdl=True,
                 vid=False,
                 input_default_bindings=True,
                 input_vo_keyboard=True,
                 osc=True)


def length(arg):
    try:
        return datetime.timedelta(seconds=arg)
    except TypeError:
        return arg


def get_data(choice):
    if "1" in choice:
        data = ["videoId", "title", "author"]
        url = "https://invidio.us/api/v1/popular"\
            f"?fields={','.join(data)}"
    elif "2" in choice:
        data = ["videoId", "title", "lengthSeconds"]
        term = "+".join(input("Search: ").split())
        url = "https://invidio.us/api/v1/search?q="\
            f"{term}&fields={','.join(data)}"
    content = json.loads(urllib.request.urlopen(url).read())
    count = 0
    video_ids = []
    for i in content:
        count += 1
        # Get first 20 results
        if count > 20:
            break
        video_ids.append(i[data[0]])
        results = f"{count}: {i[data[1]]} [{length(i[data[2]])}]"
        print(results)
    return video_ids


def video_playback(video_ids, queue_length):
    data = ["hlsUrl", "formatStreams", "title"]
    queue = 0
    for video_id in video_ids:
        queue += 1
        url = "https://invidio.us/api/v1/videos/"\
            f"{video_id}?fields={','.join(data)}"
        stream_url = json.loads(urllib.request.urlopen(url).read())
        # Try to get URL for 720p, 360p, then livestream
        try:
            url = stream_url[data[1]][1]["url"]
        except IndexError:
            try:
                url = stream_url[data[1]][0]["url"]
            except IndexError:
                url = stream_url[data[0]]
        title = stream_url[data[2]]
        print(f"[{queue} of {queue_length}] {title}")
        player.play(url)
        player.wait_for_playback()


while True:
    try:
        choice = input("1 - Popular\n2 - Search\n> ")
        video_ids = get_data(choice)
        choice = input("> ").split()
        choice_list = []
        for item in choice:
            item = int(item) - 1
            if not item > 19 and not item < 0:
                choice_list.append(item)
        video_ids = [video_ids[i] for i in choice_list]
        video_playback(video_ids, len(choice_list))
        print(r"End Of Queue ¯\_(ツ)_/¯")
    except urllib.error.HTTPError:
        print("Error While Trying To Get Video URL")
        continue
