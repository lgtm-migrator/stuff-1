import urllib.request
import datetime
import json
import mpv

player = mpv.MPV(
    ytdl=True,
    #    vid=False,
    input_default_bindings=True,
    input_vo_keyboard=True,
    osc=True)


def join(data):
    joined = ",".join(data)
    return joined


def get_json(url):
    url = json.loads(urllib.request.urlopen(url).read())
    return url


def length(seconds):
    length = datetime.timedelta(seconds=seconds)
    return length


def play(url):
    player.play(url)
    player.wait_for_playback()


def get_data(term):
    term = "+".join(term.split())
    data = ["videoId", "title", "lengthSeconds"]
    url = "https://invidio.us/api/v1/search?q="\
        f"{term}&fields={join(data)}"

    content = get_json(url)
    count = 0
    video_id = []
    for i in content:
        count += 1
        video_id.append(i[data[0]])
        results = f"{count}: {i[data[1]]} [{length(i[data[2]])}]"
        print(results)
    return video_id


def video_playback(video_ids):
    data = ["hlsUrl", "formatStreams"]
    for video_id in video_ids:
        url = "https://invidio.us/api/v1/videos/"\
            f"{video_id}?fields={join(data)}"

        stream_url = get_json(url)
        try:
            url = stream_url[data[1]][1]["url"]
        except IndexError:
            try:
                url = stream_url[data[1]][0]["url"]
            except IndexError:
                url = stream_url[data[0]]
        play(url)


while True:
    video_ids = get_data(input("Search: "))
    choice = input("> ").split()
    choice_list = []
    for item in choice:
        item = int(item) - 1
        if not item > 19 and not item < 0:
            choice_list.append(item)
    video_ids = [video_ids[i] for i in choice_list]
    video_playback(video_ids)
    print(r"End Of Queue ¯\_(ツ)_/¯")
