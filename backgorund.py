import cv2 as cv
import imutils
import os
from segmentor import Selfie_segmentation

capture = cv.VideoCapture("./videos/test.mp4")
dir = "./background"
backgrounds = []
for i in os.listdir(dir):
    backgrounds.append(cv.imread(dir + '/' + i))

background = backgrounds[0]


virtualBG = Selfie_segmentation()

while True:
    _,frame = capture.read()
    frame = cv.GaussianBlur(frame,(3,3),0)
    try:
        if Flag == False:
            bg  = cv.resize(background, (frame.shape[1], frame.shape[0]))
            outframe = virtualBG.Bg_Remover(frame, BGimg=bg, threshold=0.8, blur=(3, 3))
            cv.imshow("New Background", outframe)
        else:
            outframe = virtualBG.Bg_Remover(frame, BGimg=background, threshold=0.8, blur=(3, 3), invisible=True, frametemp=background)
            cv.imshow("New Background", outframe)
    except ValueError:
        print("Images not same size")
        print(ValueError)
        break
    except:
        print("Something else went WRONG!!")
        break

    key = cv.waitKey(20)

    if key == ord('d'):
        if i < len(backgrounds)-1:
            i += 1
            print(F"{i = }")
            Flag = False
            background = backgrounds[i]
    elif key == ord('a'):
        if i > 0:
            i -= 1
            print(F"{i = }")
            Flag = False
            background = backgrounds[i]

    elif key == ord('q'):
        break

capture.release()
cv.destroyAllWindows()