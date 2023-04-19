import ffmpeg
import numpy as np


width = 300 
height = 200


process1 = (
    ffmpeg
    .input("../videos/green.mp4")
    .output('pipe:', format='rawvideo', pix_fmt='rgb24', vframes=8)
    .run_async(pipe_stdout=True)
)

process2 = (
    ffmpeg
    .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height))
    .output("../videos/test.mp4", pix_fmt='yuv420p')
    .overwrite_output()
    .run_async(pipe_stdin=True)
)

while True:
    in_bytes = process1.stdout.read(width * height * 3)
    if not in_bytes:
        break
    in_frame = (
        np
        .frombuffer(in_bytes, np.uint8)
        .reshape([height, width, 3])
    )

    # See examples/tensorflow_stream.py:
    # out_frame = deep_dream.process_frame(in_frame)

    process2.stdin.write(
        in_frame
        .astype(np.uint8)
        .tobytes()
    )

process2.stdin.close()
process1.wait()
process2.wait()
