import sys
import os
from progressbar import ProgressBar, Percentage, Bar


def leave_error(message):
    print(message)
    quit()


def get_osu_file(path):
    for f in os.listdir(path):
        if f.endswith('.osu'):
            return path + f'\\{f}'
    return None


if len(sys.argv) < 2:
    leave_error("Error: no argument, please add path to your osu directory")

osu_dir = sys.argv[1]
if not os.path.exists(osu_dir):
    leave_error(f"Invalid path: {osu_dir}")
osu_dir = osu_dir + '\\Songs'

# Create m3u file or overwrite the existing one
if os.path.exists('osu_playlist.m3u'):
    os.remove('osu_playlist.m3u')
result = open('osu_playlist.m3u', mode='w', encoding='utf8')

pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(os.listdir(osu_dir))).start()
i = 0
for song in pbar(os.listdir(osu_dir)):
    pbar.update(i)
    i += 1
    song_dir = osu_dir + f'\\{song}'
    song_file = get_osu_file(song_dir)
    if song_file is None:
        continue
    with open(song_file, encoding='utf-8') as f:
        content = f.readlines()
    for line in content:
        if line.startswith('AudioFilename'):
            result.write(song_dir + '\\' + line.replace('AudioFilename: ', ''))
            break
pbar.finish()
