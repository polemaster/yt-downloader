import subprocess
from pytube import YouTube
import os
import datetime     # for changing seconds to hours, minutes and seconds


print('Please paste the URL of your youtube video:')
try:
    yt = YouTube(input().strip())
except Exception as exc:
    print(exc)
    exit()

system = os.name
affirmative = ['yes', 'y', 'yeah', 'да', 'tak', 'sure', 'ok', 'affirmative']
path = os.path.join(os.path.expanduser('~'), 'Downloads')   # path where all the things will be saved
# creates Downloads directory in home directory if it doesn't exist
if not os.path.isdir(path):     
    os.mkdir(path, mode=0o775)

print('Details about the video:')
print('title:', yt.title)
print('views:', yt.views)
print('author:', yt.author)
time = yt.length
length = str(datetime.timedelta(seconds = time))    # time is given in seconds so we need to convert it
print(f'length (hh:mm:ss): {length}')


# everything is enclosed in try clause to handle unexpected errors
try:
    # if there is no .mp4 format available, program exits
    streams = yt.streams.filter(file_extension='mp4', type='video', adaptive=True)
    if len(streams) == 0:
        print('No video in mp4 format available')
        exit()

    # choosing the resolution
    resolutions = sorted(set(list(map(lambda x: x.resolution, streams))))
    print('\nAvailable resolutions:', *resolutions)
    print('Please choose the desired resolution of the video.')
    res = input().strip()
    while res not in resolutions:
        print('You entered the wrong resolution. Please enter the correct one.')
        print('Available resolutions:', *resolutions)
        res = input().strip()
    streams = streams.filter(resolution=res)

    # the video codec with the highest bitrate is selected
    stream = max(streams, key=lambda x: x.bitrate)

    # the audio with the highest average bitrate (abr) is selected
    audio = yt.streams.get_audio_only()

    # ask for confirmation
    print('\nTitle:', stream.title)
    print(f'Filesize: {(stream.filesize / 1048576):.2f} MB')
    print('Do you want to download the movie? [y/n]')

    # downloading video
    if input().strip() in affirmative:
        if system == 'nt':  # if OS is Windows
            forbidden = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
            title = yt.title.translate({ord(x): '' for x in forbidden})     # removes forbidden characters in filenames on Windows
            stream.download(output_path=path, filename=title.replace(' ', '_')+'.mp4')
            audio.download(output_path=path, filename=title.replace(' ', '_')+'_audio.mp4')
        elif system == 'posix': # if OS is Linux/Mac/BSD
            forbidden = ['/']
            title = yt.title.translate({ord(x): '' for x in forbidden})     # removes forbidden characters in filenames on Linux
            stream.download(output_path=path, filename=title.replace(' ', '_')+'.mp4')
            audio.download(output_path=path, filename=title.replace(' ', '_')+'_audio.mp4')
        else:
            raise Exception('Unknown operating system')
        print(f'Success. Your video and audio have been downloaded to: {path}')

    # downloading captions
    if len(yt.captions) > 0:
        print('\nDo you want to download captions? [y/n]')
        if input().strip() in affirmative:
            languages = list(map(lambda x: x.code, yt.caption_tracks))
            print('\nAvailable languages:', *languages)
            print('Please choose the desired language code.')
            code = input().strip()
            while code not in languages:
                print('You entered the wrong language code. Please enter the correct one.')
                print('Available languages:', *languages)
                code = input().strip()
            caption = yt.captions[code]
            if system == 'nt':  # if OS is Windows
                caption.download('captions.txt', output_path=path)
            elif system == 'posix':  # if OS is Linux/Mac
                caption.download('captions.txt', output_path=path)
            else:
                raise Exception('Unknown operating system')
        print('Captions have been downloaded successfully.')

    # merging video and audio using ffmpeg software
    print('\nDo you also want to merge (combine) video and audio to one file (using ffmpeg)?  [y/n]')
    ans = input().strip()
    if ans in affirmative:
        title = title.replace(' ', '_')
        title = os.path.join(path, title)
        # there might some issues with characters like | * on linux and windows doesn't allow using quotes with ffmpeg so we fix that here
        if system == 'nt':
            cmd = f'ffmpeg -i {title}.mp4 -i {title}_audio.mp4 -c copy {title}_merged.mp4'
        else:
            cmd = f"ffmpeg -i '{title}.mp4' -i '{title}_audio.mp4' -c copy '{title}_merged.mp4'"
        subprocess.call(cmd, shell=True)
        os.remove(title + '.mp4')
        os.remove(title + '_audio.mp4')


except Exception as exc:
    print('Error:', exc)