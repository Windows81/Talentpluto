import base64
import json

from rich.markdown import Markdown
from websockets import ConnectionClosedError
from websockets.sync.client import connect
from websockets.sync.connection import Connection
import rich.console
import rich.syntax
import pyaudio
import asyncio


p = pyaudio.PyAudio()
istream = p.open(
    format=pyaudio.paFloat32,  # WHY DOES INPUT REQUIRE FLOAT32S!?!?!?!
    channels=1,
    rate=48000,
    input=True,
)
ostream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=48000,
    output=True,
)


async def read_loop(websocket: Connection, lock: asyncio.Lock):
    console = rich.console.Console()
    while True:
        try:
            await asyncio.sleep(0)
            packet: dict[str, str] = json.loads(websocket.recv(0))
            match packet.get('type', None):
                case 'websocket_audio':
                    data = base64.b64decode(packet['data'])
                    ostream.write(data)
                case 'websocket_transcript':
                    match packet['sender']:
                        case 'bot':
                            style = 'bold'
                        case _:
                            style = 'italic'
                    text = packet['text'].strip()
                    if text:
                        console.print(Markdown(text), '\n', style=style)
                case _:
                    # console.print(packet)
                    pass
        except TimeoutError:
            pass
        except ConnectionClosedError:
            return


async def write_loop(websocket: Connection, lock: asyncio.Lock):
    while True:
        try:
            await asyncio.sleep(0)
            data = istream.read(2048, False)
            async with lock:
                websocket.send(json.dumps({
                    "type": "websocket_audio",
                    "data": base64.b64encode(data).decode(),
                }))
        except ConnectionClosedError:
            return


async def main(websocket: Connection):
    websocket.send(json.dumps({
        "type": "websocket_audio_config_start",
        "input_audio_config": {
            "audio_encoding": "linear16",
            "sampling_rate": 48000,
            "audio_channel_count": 1,
            "chunk_size": 2048,
        },
        "output_audio_config": {
            "audio_encoding": "linear16",
            "sampling_rate": 48000,
            "audio_channel_count": 1,
        },
        "subscribe_transcript": True,
        "template_variables": {
            "opencall_session_id": "9bfe7d8f-0bb7-4aa4-8070-b34ce4dd8f48",
        }
    }))
    ready = websocket.recv()
    print(ready)
    lock = asyncio.Lock()
    await asyncio.gather(
        read_loop(websocket, lock),
        write_loop(websocket, lock),
    )


with connect("wss://canary.opencall.ai/websocket_call/16985") as websocket:
    asyncio.run(main(websocket))
