import cv2
import sys
#getting the name of the correct image
teren = sys.argv[1]

#getting the name of the correct image
test = sys.argv[2]

vidcap = cv2.VideoCapture('posnetki\\'+teren+'\\'+test+'.mp4')
success,image = vidcap.read()
count = 0
while success:
    cv2.imwrite("posnetki\\"+teren+"\\"+test+"\\frame%d.jpg" % count, image)     # save frame as JPEG file      
    success,image = vidcap.read()
    print('Read a new frame: ', success, count)
    count += 1
print("number of frames: ", count)
