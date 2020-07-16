import urllib.request
import datetime
import json
import mpv

player = mpv.MPV(ytdl=True,
                 input_default_bindings=True,
                 input_vo_keyboard=True,
                 vid=False,
                 osc=True)


def join(data):
    joined = ",".join(data)
    return joined


def length(seconds):
    length = datetime.timedelta(seconds=seconds)
    return length


def play(*urls):
    for url in urls:
        player.play(url)
        player.wait_for_playback()


def get_data(term):
    term = "+".join(term.split())
    data = ["videoId", "title", "lengthSeconds"]
    url = f"https://invidio.us/api/v1/search?q={term}&fields={join(data)}"
    content = json.loads(urllib.request.urlopen(url).read())
    count = 0
    video_id = []
    for i in content:
        count += 1
        video_id.append(i[data[0]])
        results = f"{count}: {i[data[1]]} [{length(i[data[2]])}]"
        print(results)
    return video_id


def video_playback(video_id):
    data = ["hlsUrl", "formatStreams"]
    video = f"https://invidio.us/api/v1/videos/{video_id}?fields={join(data)}"
    stream_url = json.loads(urllib.request.urlopen(video).read())
    try:
        url = stream_url[data[1]][1]["url"]
    except IndexError:
        try:
            url = stream_url[data[1]][0]["url"]
        except IndexError:
            url = stream_url[data[0]]
    play(url)


while True:
    video_id = get_data(input("Search: "))
    try:
        choice = int(input("> "))
    except ValueError:
        continue
    if not choice > 20 and not choice < 1:
        video_playback(video_id[choice - 1])
    print(r"End Of Queue ¯\_(ツ)_/¯")
