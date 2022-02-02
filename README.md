# twitch_clips
A python script to download a broadcaster's twitch clips.

Three variables are required to be filled in.
- client_id
- client_secret
- broadcaster_id

See https://dev.twitch.tv/docs/api/ for info on how to get client_id and client_secret

See https://www.specialagentsqueaky.com/tool/get-twitch-broadcaster-id/ for info on how to get broadcaster_id

# Running
The script will create a directory called "clips"
In this directory, it will create, in reverse chronological order starting with today, a directory for every date, and populate that directory with clips created on that dates.

The script will run until forcibly closed.