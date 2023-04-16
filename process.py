import cv2 as cv
import os
from segmentor import Selfie_segmentation

capture = cv.VideoCapture("./videos/test.mp4")
dir = "./background"
backgrounds = []
for i in os.listdir(dir):
    backgrounds.append(cv.imread(dir + '/' + i))

background = backgrounds[0]

virtualBG = Selfie_segmentation()

HEIGHT = 150
WIDTH = 150

while True:
    _,frame = capture.read()
    frame = cv.GaussianBlur(frame,(3,3),0)
    try:
        bg  = cv.resize(background, (frame.shape[1], frame.shape[0]))
        h =  HEIGHT+frame.shape[1]
        w =  WIDTH+frame.shape[0]
        corped_bg = bg[HEIGHT:h, WIDTH:w]
        print(corped_bg.shape)
        frame = cv.resize(frame, (corped_bg.shape[1], corped_bg.shape[0]))
        outframe = virtualBG.remove_bg(frame, BGimg=corped_bg, threshold=0.8, blur=(3, 3))
        cv.imshow("New Background", outframe)
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

capture.release()
cv.destroyAllWindows()