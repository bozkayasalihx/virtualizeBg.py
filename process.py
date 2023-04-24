import cv2 as cv
import os
from segmentor import FaceSegmentation

greenCapture = cv.VideoCapture("./videos/green.mp4")
backCapture = cv.VideoCapture("./videos/background.mp4")
dir = "./background"
backgrounds = []
for i in os.listdir(dir):
    backgrounds.append(cv.imread(dir + '/' + i))

background = cv.imread("./background/" + "back.jpg")
virtualBG = FaceSegmentation()

HEIGHT = 300
WIDTH = 300

fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter('output.mp4', fourcc, 30.0, (WIDTH,  HEIGHT))

print("processing..")
while greenCapture.isOpened() and backCapture.isOpened():
    gRet, greenFrame = greenCapture.read()
    bRet, backFrame = backCapture.read()

    if not gRet or not bRet:
        break
    greenFrame = cv.GaussianBlur(greenFrame, (3, 3), 0)
    backFrame = cv.GaussianBlur(backFrame, (3, 3), 0)

    try:
        greenFrame = cv.resize(greenFrame, (WIDTH, HEIGHT))
        corped_bg = backFrame[0:WIDTH, 0:HEIGHT]

        (Height, Width) = greenFrame.shape[:2]
        frame = cv.resize(greenFrame, (WIDTH, HEIGHT))

        outframe = virtualBG.remove_bg(
            frame, BGimg=corped_bg, threshold=0.8, blur=(3, 3))
        out.write(outframe)

    except ValueError:
        print("Images not same size")
        print(ValueError)
    except:
        print("Something else went WRONG!!")
    # key = cv.waitKey(20)
    # if key == ord('q'):
    #     break

print("processing done..")
greenCapture.release()
backCapture.release()
out.release()
cv.destroyAllWindows()
