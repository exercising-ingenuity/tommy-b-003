from openai import OpenAI
from gtts import gTTS
import pygame
from espeak import espeak
import os
from pathlib import Path
from dotenv import load_dotenv
#from IPython.display import Audio

dotenv_path = Path('/home/tommy_b/Downloads/.env')

# Load the .env file
load_dotenv(dotenv_path=dotenv_path)

# Access api key
api_key = os.environ.get("OPEN_API_KEY")

def speak(text):
	tts = gTTS(text, lang="en", tld="co.uk")
	tts.save("audio_reply.wav")
	sound_file = "audio_reply.wav"
	#wn = Audio(sound_file, autoplay=True)
	#display(wn)
	pygame.mixer.init()
	pygame.mixer.music.load("audio_reply.wav")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
		continue

client = OpenAI(
	api_key
)

messages = [
	{
		"role": "system",
		"content": "You are a moody AI"
	}
]

while True:
	message = input("You: ")

	messages.append(
		{
			"role": "user",
			"content": message
		},
	)

	chat = client.chat.completions.create(
		messages=messages,
		model="gpt-3.5-turbo"
	)

	reply = chat.choices[0].message

	#speak(reply.content)
	#flite -t reply.content -o audio_reply.wav
	c#vlc audio_reply.wav

	print("Assitant: ", reply.content)

	messages.append(reply)		
