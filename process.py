import cv2 as cv
import os
from segmentor import FaceSegmentation
import ffmpeg 

greenCapture = cv.VideoCapture("./videos/green.mp4")
backCapture = cv.VideoCapture("./videos/background.mp4")
dir = "./background"
backgrounds = []
for i in os.listdir(dir):
    backgrounds.append(cv.imread(dir + '/' + i))

background = cv.imread("./background/" + "back.jpg")
virtualBG = FaceSegmentation()

HEIGHT = 150
WIDTH = 150

fourcc = cv.VideoWriter_fourcc(*'MJPG')
output = cv.VideoWriter(
    "output.avi", cv.VideoWriter_fourcc(*'MPEG'), 30, (1080, 1920))


curIndex = 0

while True:
    _, greenFrame = greenCapture.read()
    _, backFrame = backCapture.read()
    greenFrame = cv.GaussianBlur(greenFrame, (3, 3), 0)
    backFrame = cv.GaussianBlur(backFrame, (3, 3), 0)
    try:
        greenFrame = cv.resize(greenFrame, (300, 300))
        corped_bg = backFrame[0:WIDTH, 0:HEIGHT]
        (Height, Width) = greenFrame.shape[:2]
        frame = cv.resize(greenFrame, (corped_bg.shape[0], corped_bg.shape[1]))
        outframe = virtualBG.remove_bg(
            frame, BGimg=corped_bg, threshold=0.8, blur=(3, 3))
        
        ffmpeg.input()


        # cv.imshow("New Background", outframe)
    except ValueError:
        print("Images not same size")
        print(ValueError)
        break
    except:
        print("Something else went WRONG!!")
        break

    key = cv.waitKey(20)
    if key == ord('q'):
        break

greenCapture.release()
backCapture.release()
cv.destroyAllWindows()
