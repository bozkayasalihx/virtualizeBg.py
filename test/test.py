import cv2 as cv
import datetime
  
# img = cv2.imread("./background/back.jpg")
  
# print("Shape of the image", img.shape)
  
# crop = img[50:180, 100:300]  
  
# cv2.imshow('original', img)
# cv2.imshow('cropped', crop)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


class Save:
    def __init__(self,name,fourcc=-1,Winsize=(640, 480)):
        time_stamp = datetime.datetime.now().strftime('%y-%m-%d-%H-%M')

        name = f'{name}-{time_stamp}'
        self.Videofile = cv.VideoWriter(f'{name}.mp4', fourcc, 20.0, Winsize)

        print("Video Saving initialized")

    def videoSaver(self,frame):
        self.Videofile.write(frame)



capture = cv.VideoCapture("/home/malware/test/videos/woman.mp4")
save = Save("maker", -1, (300, 300))

while True:
    _,frame = capture.read()
    frame = cv.GaussianBlur(frame,(3,3),0)
    # frame = cv.resize(frame, (300, 300))
    save.videoSaver(frame)
    key = cv.waitKey(20)

    if key == ord('q'):
        break

capture.release()
cv.destroyAllWindows()