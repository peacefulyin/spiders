from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=k2qgadSvNyU')
print(yt.get_videos())

#video = yt.get('mp4')
#print(video)
video = yt.filter('mp4')[-1]

yt.set_filename('first')
video.download('./')
