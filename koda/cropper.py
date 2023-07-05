# python croper.py teren2AB testA890539 testB839215_aligned t2A t2B
# python croper.py teren3AB testA704380 testB652675_aligned t3A t3B
# python croper.py teren4AB testA497269 testB445598_aligned t4A t4B
# python croper.py teren5AB testA230478 testB178720_aligned t5A t5B
# python croper.py teren6AB testA675803 testB623652_aligned t6A t6B
from asyncio import FIRST_COMPLETED
import cv2
import sys
import numpy as np


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


#getting the name of the correct image
teren = sys.argv[1]

#getting the name of the correct image
test1 = sys.argv[2] #A slike og
test2 = sys.argv[3] #B slike aligned
test3 = sys.argv[4] #new A slike
test4 = sys.argv[5] #new B slike
#Read the image, convert it into grayscale, and make in binary image for threshold value of 1.

img = cv2.imread("posnetki\\"+teren+"\\"+test2+"\\frame1.jpg")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)


x ,y ,w ,h = cv2.boundingRect(thresh) 

print("x: "+str(x)+" y: "+str(y)+" x2: " +str(img.shape[1] -(x+w))+" y2: "+str(img.shape[0] -(y+h)))
#Now crop the image, and save it into another file.
x = 31 #x crop of leftmost pixel 
y = 0 #y crop of topmost pixel
x2 = 0 #x crop from rightmost pixel
y2 = 12 #y crop from bottommost pixel

# no crop
#x,y,x2,y2 = 0,0,0,0

w = img.shape[1] - x - x2 #width of cropped image
h = img.shape[0] - y - y2 #height of cropped image

l = 7508 #length of the video
#l = 10
for count in range(1,l +1):
    
    img = cv2.imread("posnetki\\"+teren+"\\"+test2+"\\frame"+str(count)+".jpg")
    crop = img[y:y+h,x:x+w]
    cv2.imwrite("posnetki\\" + teren + "\\" + test4 + "\\frameC%d.jpg" % count , crop)

    img = cv2.imread("posnetki\\"+teren+"\\"+test1+"\\frame"+str(count)+".jpg")
    crop = img[y:y+h,x:x+w]
    cv2.imwrite("posnetki\\" + teren + "\\" + test3 + "\\frameC%d.jpg" % count , crop)
    #print("frame"+str(count)+" done")
    printProgressBar(count, l, prefix = 'Progress:', suffix = 'Complete ' + str(count), length = 50)
