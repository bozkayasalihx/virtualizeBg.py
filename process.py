import cv2 as cv
from segmentor import FaceSegmentation
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import tempfile
import shutil
import subprocess


class Processor(FaceSegmentation):
    x, y, w, h = 0, 0, 400, 400

    def __init__(self, foreground: str, background: str) -> None:
        self.foreground = foreground
        self.background = background
        self.tempdir = tempfile.mkdtemp()
        self.curDir = os.getcwd()
        self.foreSampled = "foreSampled.mp4"
        self.backSampled = "backSampled.mp4"
        self.outSampled = "output.mp4"
        super().__init__()

    def min(self, x: int, y: int):
        if x < y:
            return x
        return y

    def prep(self):
        path = self.tempdir
        foreGround = VideoFileClip(self.foreground)
        backGround = VideoFileClip(self.background)
        fps = self.min(foreGround.fps, backGround.fps)
        self.fps = fps
        foreSampled = foreGround.set_fps(fps)
        backSampled = backGround.set_fps(fps)
        forPath = os.path.join(path, self.foreSampled)
        backPath = os.path.join(path, self.backSampled)
        foreSampled.write_videofile(forPath)
        backSampled.write_videofile(backPath)

        return forPath, backPath

    def convert(self):
        backPath = self.tempdir + "/" + self.backSampled
        outPath = self.tempdir + "/" + self.outSampled
        subprocess.run(["ffmpeg", "-i", backPath, "-i", outPath, "-r", str(self.fps),
                       "-c:a", "copy", "-filter_complex", f"[0:v][1:v]overlay={self.x}:{self.y}", "out.mp4"])
        shutil.rmtree(self.tempdir)

    def outPath(self):
        forTemp = os.path.join(self.tempdir, "output.mp4")
        return forTemp

    def process(self):
        (fore, back) = self.prep()

        outPath = self.outPath()

        foreCapture = cv.VideoCapture(fore)
        backCapture = cv.VideoCapture(back)
        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        fFps = int(foreCapture.get(cv.CAP_PROP_FPS))
        bFps = int(backCapture.get(cv.CAP_PROP_FPS))

        out = cv.VideoWriter(outPath, fourcc,
                             self.min(fFps, bFps), (self.w, self.h))

        print("processing")

        while foreCapture.isOpened() and backCapture.isOpened():
            gRet, foreFrame = foreCapture.read()
            bRet, backFrame = backCapture.read()

            if not gRet or not bRet:
                break
            foreFrame = cv.GaussianBlur(foreFrame, (3, 3), 0)
            backFrame = cv.GaussianBlur(backFrame, (3, 3), 0)

            try:
                foreFrame = cv.resize(foreFrame, (self.w, self.h))
                roi = backFrame[self.x:self.x + self.w, self.y: self.y+self.h]
                outFrame = self.remove_bg(
                    foreFrame, roi, threshold=0.8, blur=(3, 3))
                out.write(outFrame)

            except ValueError:
                print("Images not same size")
                print(ValueError)
            except:
                print("Something else went WRONG!!")

        foreCapture.release()
        backCapture.release()
        out.release()
        cv.destroyAllWindows()
        self.convert()

        print("processing done... ")


if __name__ == "__main__":
    foreInput = "./videos/green.mp4"
    backInput = "./videos/background.mp4"
    processor = Processor(foreground=foreInput, background=backInput)
    processor.process()
