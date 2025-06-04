#MULTITHREADING import
import threading

#SERVO import
import time
import random
from adafruit_servokit import ServoKit

#PERSONSENSOR import
import io
import fcntl
import struct

########## SERVO setup ##########
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

num_servos = 6

########## PERSON SENSOR setup ##########
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

i2c_handle = io.open("/dev/i2c-" + str(I2C_CHANNEL), "rb", buffering=0)
fcntl.ioctl(i2c_handle, I2C_PERIPHERAL, PERSON_SENSOR_I2C_ADDRESS)

########## SERVO functions ##########
class Servo:
	def __init__(self, servo, max, min, neutral):
		self.servo = servo
		self.max = max
		self.min = min
		self.neutral = neutral

# Servo calibrations
upper_eyelid = Servo(0, 140, 80, 90)
lower_eyelid = Servo(1, 140, 80, 90)
right_eye_h = Servo(2, 120, 20, 70)
right_eye_v = Servo(3, 120, 20, 80)
left_eye_h = Servo(4, 140, 30, 90)
left_eye_v = Servo(5, 120, 60, 90)


def basic_test_servo():
	kit.servo[0].angle = 180
	kit.continuous_servo[1].throttle = 1
	time.sleep(1)
	kit.continuous_servo[1].throttle = -1
	time.sleep(1)
	kit.servo[0].angle = 0
	kit.continuous_servo[1].throttle = 0

def move_all_servos():
    kit.servo[0].angle = 100
    kit.servo[1].angle = 100
    kit.servo[2].angle = 100
    kit.servo[3].angle = 100
    kit.servo[4].angle = 100
    kit.servo[5].angle = 100
    time.sleep(1)
    kit.servo[0].angle = 80
    kit.servo[1].angle = 80
    kit.servo[2].angle = 80
    kit.servo[3].angle = 80
    kit.servo[4].angle = 80
    kit.servo[5].angle = 80
    time.sleep(1)

def all_servos_neutral():
	kit.servo[upper_eyelid.servo].angle = upper_eyelid.neutral
	kit.servo[lower_eyelid.servo].angle = lower_eyelid.neutral
	kit.servo[right_eye_h.servo].angle = right_eye_h.neutral
	kit.servo[right_eye_v.servo].angle = right_eye_v.neutral
	kit.servo[left_eye_h.servo].angle = left_eye_h.neutral
	kit.servo[left_eye_v.servo].angle = left_eye_v.neutral

def eye_servos_neutral():
	kit.servo[right_eye_h.servo].angle = right_eye_h.neutral
	kit.servo[right_eye_v.servo].angle = right_eye_v.neutral
	kit.servo[left_eye_h.servo].angle = left_eye_h.neutral
	kit.servo[left_eye_v.servo].angle = left_eye_v.neutral

def move_one_servo(servo):
	kit.servo[servo].angle = 90
	time.sleep(1)
	kit.servo[servo].angle = 95
	time.sleep(1)
	kit.servo[servo].angle = 85
	time.sleep(1)
	kit.servo[servo].angle = 90
	time.sleep(1)

def close_eyes():
	kit.servo[upper_eyelid.servo].angle = upper_eyelid.max
	kit.servo[lower_eyelid.servo].angle = lower_eyelid.max

def open_eyes():
	kit.servo[upper_eyelid.servo].angle = upper_eyelid.min
	kit.servo[lower_eyelid.servo].angle = lower_eyelid.min

def eyes_right():
	kit.servo[right_eye_h.servo].angle = right_eye_h.min
	kit.servo[left_eye_h.servo].angle = left_eye_h.min

def eyes_left():
	kit.servo[right_eye_h.servo].angle = right_eye_h.max
	kit.servo[left_eye_h.servo].angle = left_eye_h.max
	
def eyes_up():
	kit.servo[right_eye_v.servo].angle = right_eye_v.min
	kit.servo[left_eye_v.servo].angle = left_eye_v.max

def eyes_dw():
	kit.servo[right_eye_v.servo].angle = right_eye_v.max
	kit.servo[left_eye_v.servo].angle = left_eye_v.min

def blink(min_delay, max_delay, iterations):
	
	for i in range(iterations):
		close_eyes()
		blink_pause = random.uniform(0.14, 0.15)
		time.sleep(blink_pause)
		open_eyes()
		delay = random.uniform(min_delay, max_delay)
		time.sleep(delay)

def eyes_look():

	for i in range(10):
		pause = 0.5
		eyes_right()
		time.sleep(pause)
		eyes_left()
		time.sleep(pause)
		eye_servos_neutral()
		time.sleep(pause)
		eyes_up()
		time.sleep(pause)
		eyes_dw()
		time.sleep(pause)
		eye_servos_neutral()

########## PERSON SENSOR functions ##########
def person_sensor(iterations, person_sensor_delay):
	n=0
	while n<iterations:
		try:
			read_bytes = i2c_handle.read(PERSON_SENSOR_RESULT_BYTE_COUNT)
		except OSError as error:
			print("No person sensor data found")
			print(error)
			time.sleep(person_sensor_delay)
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
		print(num_faces, faces)
		n += 1
		time.sleep(person_sensor_delay)

########## TEST functions ##########
# TEST FUNCTION - full range of motion for eyes
def test_servos():

	pause = 0.5
	close_eyes()
	time.sleep(pause)
	open_eyes()
	time.sleep(pause)
	eyes_right()
	time.sleep(pause)
	eyes_left()
	time.sleep(pause)
	all_servos_neutral()
	time.sleep(pause)
	eyes_up()
	time.sleep(pause)
	eyes_dw()
	time.sleep(pause)
	all_servos_neutral()

# TEST FUNCTION - robot moves eyes and blinks multiple times
def test_blink():
	print("Begin blink program")
	
	time.sleep(3)
	
	eyes_right()
	
	min_delay = 1
	max_delay = 4
	iterations = 10
	
	for i in range(iterations):
		blink()
		delay = random.uniform(min_delay, max_delay)
		
		eyes_left()
		
		time.sleep(delay)
	
	all_servos_neutral()
	print("End blink program")

# TEST FUNCTION - test looking
def test_look():

	for i in range(10):
		pause = 0.5
		eyes_right()
		time.sleep(pause)
		eyes_left()
		time.sleep(pause)
		eye_servos_neutral()
		time.sleep(pause)
		eyes_up()
		time.sleep(pause)
		eyes_dw()
		time.sleep(pause)
		eye_servos_neutral()


if __name__ == "__main__":
	
	#test_servos()

	# blink variables
	min_delay = 1
	max_delay = 4
	iterations = 5
	# blink thread
	t_blink = threading.Thread(target=blink, args=(min_delay, max_delay, iterations))
	
	# eyes look thread
	t_look = threading.Thread(target=eyes_look, args=())

	# person sensor variables
	person_sensor_delay = 0.4# How long to pause between sensor polls.
	# person sensor thread
	t_person_sensor = threading.Thread(target=person_sensor, args=(iterations, person_sensor_delay))

	#blink(min_delay,max_delay,iterations)
	#eyes_look()
	#person_sensor()

	# START THREADS
	t_blink.start()
	t_look.start()
	t_person_sensor.start()

	# END THREADS
	t_blink.join()
	t_look.join()
	t_person_sensor.join()
