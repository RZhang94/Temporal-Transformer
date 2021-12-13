import os

os.chdir(r'C:\test')
print(os.getcwd())
read = r'C:\test\Vid\frame_%01d.png'
target = r'C:\test\Vid\test.mp4'
os.system('ffmpeg -f image2 -r 10 -i '+ read+ ' -vcodec mpeg4 -y ' + target)