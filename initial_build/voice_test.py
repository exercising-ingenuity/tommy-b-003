import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

num_servos = 6

class Servo:
	def __init__(self, servo, max, min, neutral):
		self.servo = servo
		self.max = max
		self.min = min
		self.neutral = neutral

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




if __name__ == "__main__":
	
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
	
	#basic_test_servo()
	#all_servos_neutral()
	#i=0
	#move_all_servos()
	#while i<3:
	#	move_all_servos()
	#	i = i+1
	#all_servos_neutral()
	
	
	#move_one_servo(0)
	#move_one_servo(1)
