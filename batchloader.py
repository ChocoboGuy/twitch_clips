import re
import urllib.request
import requests
import sys
import datetime
import os
import random
import time

# Variables to fill-in
client_id = ""
client_secret = ""
broadcaster_id = 0

basepath = 'downloads/'
base_clip_path = 'https://clips-media-assets2.twitch.tv/'

def retrieve_mp4_data(clip_info):
    thumb_url = clip_info['thumbnail_url']
    title = clip_info['title']
    slice_point = thumb_url.index("-preview-")
    mp4_url = thumb_url[:slice_point] + '.mp4'
    return mp4_url, title


def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()


# 
# This section requests a unique access token using client_id and client_secret, you sign up for those on the twitch site 
#
token = requests.post("https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials".format(client_id, client_secret)).json()
print(token['access_token'])

today = datetime.datetime.now()
today += datetime.timedelta(days = +1)
yesterday = today + datetime.timedelta(days = -1)

# This loop will loop over every day in reverse, starting with today
# There is no exit to this loop, you have to ctrl+z out of the script

while True:
    # Creates a timestamp variable in ISO form for "today" and "yesterday"
    today += datetime.timedelta(days = -1)
    yesterday += datetime.timedelta(days = -1)
    todayISO = today.isoformat() + "Z"
    yesterdayISO = yesterday.isoformat() + "Z"

    # Get a list of Broadcaster's clips for a 24 hour period (max of 100 clips), note her broadcaster id
    clipList = requests.get(
        "https://api.twitch.tv/helix/clips?broadcaster_id={}&first=100&started_at={}&ended_at={}".format(broadcaster_id, yesterdayISO, todayISO),
        headers={"Client-ID": "{}".format(client_id), "Authorization": "Bearer {}".format(token['access_token'])}).json()

    # Make a directory called "clips" if it does not already exist
    basepath = "clips"
    if not os.path.isdir("clips"):
        os.mkdir("clips")

    print(yesterdayISO[:10])
    print(len(clipList['data']))
    time.sleep(1)

    # Make a directory of the date, if it does not already exist
    if (len(clipList['data'])):
        basepath = os.path.join("clips", yesterdayISO[:10])
        print(basepath)
        if not os.path.isdir(basepath):
            os.mkdir(basepath)

    # for each clip in clips.txt
    # do regex magic to rename the file to a name that the file system can handle
    for clip in clipList['data']:
        mp4_url, clip_title = retrieve_mp4_data(clip)
        regex = re.compile('[^a-zA-Z0-9_]')
        clip_title = clip_title.replace(' ', '_')
        out_filename = regex.sub('', clip_title) + '.mp4'
        output_path = os.path.join(basepath, out_filename)

        # Duplicate name checking, if the name already exists it will append a random number
        if os.path.exists(output_path):
            out_filename = str(random.randrange(0, 10000)) + out_filename
            output_path = os.path.join(basepath, out_filename)
        
        # Print out the filename, and download it
        print('"' + clip_title + '" -> ' + out_filename)
        print(mp4_url)
        urllib.request.urlretrieve(mp4_url, output_path, reporthook=dl_progress)
        print('\nDone.')
