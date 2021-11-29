import cv2
import subprocess
import pyaudio

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Stream Audio data here
# data = stream.read(CHUNK)


cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 30

command = ['ffmpeg',
           '-y',
           '-f', 'rawvideo',
           '-pixel_format', 'bgr24',
           '-video_size', "{}x{}".format(width, height),
           '-framerate', str(fps),
           '-i', 'pipe:0',
           '-re',
           '-f', 'lavfi',
           '-i', 'pipe:1',
           '-c:v', 'libx264',
           '-c:a', 'aac',
           '-vf', 'format=yuv420p',
           '-f', 'flv',
            ]


pipe = subprocess.Popen(command, shell=False, stdin=subprocess.PIPE
)
while cap.isOpened():
    success, frame = cap.read()
    if success:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        pipe.stdin.write(frame.tostring())
        pipe.stdin.write(stream.read(CHUNK))

stream.stop_stream()
stream.close()
p.terminate()
cap.release()
pipe.terminate()
