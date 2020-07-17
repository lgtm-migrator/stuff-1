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
        # Get First 20 Results
        if count > 20:
            break
        video_ids.append(i[data[0]])
        results = f"{count}: {i[data[1]]} [{length(i[data[2]])}]"
        print(results)
    return video_ids


def video_playback(video_ids):
    data = ["hlsUrl", "formatStreams"]
    for video_id in video_ids:
        url = "https://invidio.us/api/v1/videos/"\
            f"{video_id}?fields={','.join(data)}"
        stream_url = json.loads(urllib.request.urlopen(url).read())
        # Try To Get 720p Link, Then 360p. Else, Get Livestream Link
        try:
            url = stream_url[data[1]][1]["url"]
        except IndexError:
            try:
                url = stream_url[data[1]][0]["url"]
            except IndexError:
                url = stream_url[data[0]]
        player.play(url)
        player.wait_for_playback()


while True:
    try:
        choice = input("1 - Show Popular\n2 - Search\n> ")
        video_ids = get_data(choice)
        choice = input("> ").split()
        choice_list = []
        for item in choice:
            item = int(item) - 1
            if not item > 19 and not item < 0:
                choice_list.append(item)
        video_ids = [video_ids[i] for i in choice_list]
        video_playback(video_ids)
        print(r"End Of Queue ¯\_(ツ)_/¯")
    except urllib.error.HTTPError:
        print("Error While Trying To Get Video URL")
        continue
