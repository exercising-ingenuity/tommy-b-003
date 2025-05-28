# Example of accessing the Person Sensor from Useful Sensors on a Pi using
# Python. See https://usfl.ink/ps_dev for the full developer guide.

import io
import fcntl
import struct

import time
from adafruit_servokit import ServoKit
import subprocess

import wave
import sys
import pyaudio

# The person sensor has the I2C ID of hex 62, or decimal 98.
PERSON_SENSOR_I2C_ADDRESS = 0x62

# We will be reading raw bytes over I2C, and we'll need to decode them into
# data structures. These strings define the format used for the decoding, and
# are derived from the layouts defined in the developer guide.
PERSON_SENSOR_I2C_HEADER_FORMAT = "BBH"
PERSON_SENSOR_I2C_HEADER_BYTE_COUNT = struct.calcsize(
    PERSON_SENSOR_I2C_HEADER_FORMAT)

PERSON_SENSOR_FACE_FORMAT = "BBBBBBbB"
PERSON_SENSOR_FACE_BYTE_COUNT = struct.calcsize(PERSON_SENSOR_FACE_FORMAT)

PERSON_SENSOR_FACE_MAX = 4
PERSON_SENSOR_RESULT_FORMAT = PERSON_SENSOR_I2C_HEADER_FORMAT + \
    "B" + PERSON_SENSOR_FACE_FORMAT * PERSON_SENSOR_FACE_MAX + "H"
PERSON_SENSOR_RESULT_BYTE_COUNT = struct.calcsize(PERSON_SENSOR_RESULT_FORMAT)

# I2C channel 1 is connected to the GPIO pins
I2C_CHANNEL = 1
I2C_PERIPHERAL = 0x703

# How long to pause between sensor polls.
PERSON_SENSOR_DELAY = 0.4

i2c_handle = io.open("/dev/i2c-" + str(I2C_CHANNEL), "rb", buffering=0)
fcntl.ioctl(i2c_handle, I2C_PERIPHERAL, PERSON_SENSOR_I2C_ADDRESS)

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

wav_filepath = '/home/tommy_b/openai/testing/i_see_you.wav'

def play_audio(file_path):
    # Open the audio file
    wf = wave.open(file_path, 'rb')
    
    # Create PyAudio instance
    p = pyaudio.PyAudio()
    
    # Open a stream to play audio
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    # Read and play audio data
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)
        
    # Stop and close the stream and PyAudio instance
    stream.stop_stream()
    stream.close()
    p.terminate()
    
def move_servo():
    kit.servo[0].angle = 150
    kit.continuous_servo[1].throttle = 1
    time.sleep(1)
    kit.continuous_servo[1].throttle = -1
    time.sleep(1)
    kit.servo[0].angle = 50
    kit.continuous_servo[1].throttle = 0
    
def move_all_servos():
    kit.servo[0].angle = 180
    kit.servo[1].angle = 180
    kit.servo[2].angle = 180
    kit.servo[3].angle = 180
    kit.servo[4].angle = 180
    kit.servo[5].angle = 180
    time.sleep(1)
    kit.servo[0].angle = 0
    kit.servo[1].angle = 0
    kit.servo[2].angle = 0
    kit.servo[3].angle = 0
    kit.servo[4].angle = 0
    kit.servo[5].angle = 0
    time.sleep(1)

while True:
    try:
        read_bytes = i2c_handle.read(PERSON_SENSOR_RESULT_BYTE_COUNT)
    except OSError as error:
        print("No person sensor data found")
        print(error)
        time.sleep(PERSON_SENSOR_DELAY)
        continue
    offset = 0
    (pad1, pad2, payload_bytes) = struct.unpack_from(
        PERSON_SENSOR_I2C_HEADER_FORMAT, read_bytes, offset)
    offset = offset + PERSON_SENSOR_I2C_HEADER_BYTE_COUNT

    (num_faces) = struct.unpack_from("B", read_bytes, offset)
    num_faces = int(num_faces[0])
    offset = offset + 1

    faces = []
    for i in range(num_faces):
        (box_confidence, box_left, box_top, box_right, box_bottom, id_confidence, id,
         is_facing) = struct.unpack_from(PERSON_SENSOR_FACE_FORMAT, read_bytes, offset)
        offset = offset + PERSON_SENSOR_FACE_BYTE_COUNT
        face = {
            "box_confidence": box_confidence,
            "box_left": box_left,
            "box_top": box_top,
            "box_right": box_right,
            "box_bottom": box_bottom,
            "id_confidence": id_confidence,
            "id": id,
            "is_facing": is_facing,
        }
        faces.append(face)
    checksum = struct.unpack_from("H", read_bytes, offset)
    #print(num_faces, faces)
    move_all_servos()
    
    if num_faces > 0:
        #print("I see you")
        play_audio(wav_filepath)	    
        #move_servo()
        
    time.sleep(PERSON_SENSOR_DELAY)
