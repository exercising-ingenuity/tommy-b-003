import asyncio
import websockets
import sounddevice as sd
import numpy as np
import json
import base64
import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path('/home/tommy_b/Downloads/.env')

# Load te h.env file
load_dotenv(dotenv_path=dotenv_path)

# Access api key
OPENAI_API_KEY = os.environ.get("OPEN_API_KEY")

# Audio settings
INPUT_SAMPLE_RATE = 16000
OUTPUT_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024
SILENCE_TIMEOUT_MS = 5000  # 3 seconds of silence before Tommy responds
# Tommy personality & audio settings
SYSTEM_PROMPT = (
    "You are Tommy-B-003, a witty, sarcastic, slightly passive aggressive robot. "
    "Be freindly, but don't be afraid to joke, poke fun  the user, make jibes at the user, or use sarcasm. "
    "You must speak ONLY in English"
    "Never respond in any other languages and do not translate or improvise in another language."
    "Speak clearly, pause naturally, and answer questions concisely. "
)
VOICE_SETTINGS = {
    "voice": "verse",       # Options: 'aria', 'alloy', 'verse', etc.
    "style": "cheerful",   # Optional: 'calm', 'cheerful', 'excited'
    "pitch": 0.8,
    "rate": 1.0
}

# Minimum volume to consider as speech (ignore ambient noise)
NOISE_THRESHOLD = 500

# -----------------------------
# AUDIO HANDLER
# -----------------------------
class AudioHandler:
    def __init__(self, ws, loop):
        self.ws = ws
        self.loop = loop
        self.silence_counter = 0
        self.speaking = False

    def input_callback(self, indata, frames, time, status):
        if status:
            print("Input status:", status)

        # Measure volume to ignore quiet ambient noise
        volume = np.abs(indata).mean()
        if volume < NOISE_THRESHOLD:
            if self.speaking:
                self.silence_counter += 1
        else:
            self.speaking = True
            self.silence_counter = 0

        # Send audio chunk to server
        audio_bytes = indata.tobytes()
        encoded = base64.b64encode(audio_bytes).decode("utf-8")
        asyncio.run_coroutine_threadsafe(
            self.ws.send(json.dumps({"type": "input_audio_buffer.append", "audio": encoded})),
            self.loop
        )

    async def monitor_silence(self):
        """Commit audio buffer and trigger AI response after silence."""
        while True:
            if self.speaking and self.silence_counter * (CHUNK_SIZE / INPUT_SAMPLE_RATE * 1000) > SILENCE_TIMEOUT_MS:
                # Commit audio buffer
                await self.ws.send(json.dumps({"type": "input_audio_buffer.commit"}))

                # Trigger AI response with system prompt and voice settings
                await self.ws.send(json.dumps({
                    "type": "response.create",
                    "response": {
                        "modalities": ["audio"],
                        "instructions": SYSTEM_PROMPT,
                        "audio": VOICE_SETTINGS
                    }
                }))

                self.speaking = False
                self.silence_counter = 0
            await asyncio.sleep(0.05)

# -----------------------------
# SEND AUDIO TO SERVER
# -----------------------------
async def send_audio(ws, loop):
    handler = AudioHandler(ws, loop)
    with sd.InputStream(
        samplerate=INPUT_SAMPLE_RATE,
        channels=1,
        dtype="int16",
        blocksize=CHUNK_SIZE,
        callback=handler.input_callback
    ):
        await handler.monitor_silence()

# -----------------------------
# RECEIVE AI AUDIO
# -----------------------------
async def receive_audio(ws):
    output_stream = sd.OutputStream(
        samplerate=OUTPUT_SAMPLE_RATE,
        channels=1,
        dtype="float32",
        blocksize=CHUNK_SIZE
    )
    output_stream.start()

    while True:
        message = await ws.recv()
        data = json.loads(message)

        if data.get("type") == "response.audio.delta":
            audio_chunk = base64.b64decode(data["delta"])
            audio_np = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0
            audio_np *= 1.5
            audio_np = np.clip(audio_np, -1.0, 1.0)
            output_stream.write(audio_np)

        if data.get("type") == "response.completed":
            print("🤖 Tommy finished speaking.")

# -----------------------------
# MAIN REALTIME LOOP
# -----------------------------
async def main():
    loop = asyncio.get_running_loop()
    url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Beta": "realtime=v1"
    }

    async with websockets.connect(url, extra_headers=headers) as ws:
        print("✅ Connected to OpenAI Realtime API")

        # Server-side VAD as a backup
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "turn_detection": {
                    "type": "server_vad",
                    "silence_timeout_ms": SILENCE_TIMEOUT_MS
                }
            }
        }))
        
        print("🎤 Tommy-B-003 is listening...")

        await asyncio.gather(
            send_audio(ws, loop),
            receive_audio(ws)
        )

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    asyncio.run(main())