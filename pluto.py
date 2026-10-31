import asyncio
import json
import time
import uuid

import rich.pretty
import rich.markdown
import rich.console
import livekit.rtc
import rich.jupyter
import rich.live
import requests

cookies = {
    '__Secure-better-auth.session_token': 'SEltLlCipBhK7C1dGEYm9owT6cMNJN1U.Nv3guviYHmGtX8I8k9cRJUYMV7ThZuEocpm2C3ve7xI%3D',
    '__Secure-better-auth.session_data': 'eyJzZXNzaW9uIjp7InNlc3Npb24iOnsiaWQiOiJkMzMzNTUwMi05OWEzLTQxNGEtODY3ZS03N2U0ZDI4ZjhlNjgiLCJ0b2tlbiI6IlNFbHRMbENpcEJoSzdDMWRHRVltOW93VDZjTU5KTjFVIiwidXNlcklkIjoiOWQwNzc4ZTctZmM5ZC00MDM4LWFmY2EtZDU5N2UxNjZlYWVmIiwiZXhwaXJlc0F0IjoiMjAyNi0xMC0yNFQwMDoyODo1MC45MTRaIiwiY3JlYXRlZEF0IjoiMjAyNi0xMC0xN1QwMDoyODo1MC4wOTJaIiwidXBkYXRlZEF0IjoiMjAyNi0xMC0xN1QwMDoyODo1MC45MTRaIiwiaXBBZGRyZXNzIjoiIiwidXNlckFnZW50IjoiIiwiYWN0aXZlT3JnYW5pemF0aW9uSWQiOm51bGx9LCJ1c2VyIjp7ImlkIjoiOWQwNzc4ZTctZmM5ZC00MDM4LWFmY2EtZDU5N2UxNjZlYWVmIiwiZW1haWwiOiJwcmVzc0B4LnhvbSIsImVtYWlsVmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiVW5rbm93biBVc2VyIiwiaW1hZ2UiOm51bGwsInJvbGUiOiJjYW5kaWRhdGUiLCJjcmVhdGVkQXQiOiIyMDI2LTA1LTA3VDAzOjQ0OjEyLjYyOFoiLCJ1cGRhdGVkQXQiOiIyMDI2LTEwLTA3VDIxOjQwOjA1LjczMloifSwidXBkYXRlZEF0IjoxNzkyMjAwNjIwNzk0LCJ2ZXJzaW9uIjoiMSJ9LCJleHBpcmVzQXQiOjE3OTIyMDA5MjA3OTQsInNpZ25hdHVyZSI6IkJwRm5keWlOa182OVN2VHl0S0Q3Wk9YOW9ISXNYaGZNSjczOWFIaGp4X1EifQ',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,enq=0.9,esq=0.8',
    # 'content-length': '0',
    'dnt': '1',
    'origin': 'https://app.talentpluto.com',
    'priority': 'u=1, i',
    'referer': 'https://app.talentpluto.com/talent/chat',
    'sec-ch-ua': '"Not)ABrand"v="8", "Chromium"v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}


def start_call():
    CALL_FILE = '_pluto_call_auth'

    now = time.time()
    try:
        f = open(CALL_FILE, 'r')
        if now < float(f.readline()):
            return json.load(f)
    except FileNotFoundError, ValueError:
        pass

    '''
    Example:
    {
        "url": "wss://phonic-sts-star5ptw.livekit.cloud",
        "token": "eyJhbGciOiJIUzI1NiJ9.eyJ2aWRlbyI6eyJyb29tIjoiUGhvbmljLUNvbnZlcnNhdGlvbi01YmFhOWUzMS1jZTE3LTRiNTAtODgxZi05MzUwYjUxMDU3ZmIiLCJyb29tSm9pbiI6dHJ1ZSwiY2FuUHVibGlzaCI6dHJ1ZSwiY2FuU3Vic2NyaWJlIjp0cnVlfSwiaXNzIjoiQVBJbnJHQTdjUUxpenFWIiwiZXhwIjoxNzkyMjAyMzY1LCJuYmYiOjE3OTIyMDIzMDUsInN1YiI6ImNsaWVudC0zMzJmNTdjYS00MTkxLTRkZGMtYTUwMS1kYWFiMjdmNjM5ODYifQ.U8Y2HgXNzsT6-BtG_2dV_BhdJXCPFeRmnlvX9h7hmPU",
        "callId": "web-call-reservation:95c631b9-eded-45b8-a4de-24f1d59a08fb",
        "expiresInSeconds": 30,
        "success": true,
        "timings": {
            "authMs": 100,
            "requestRateLimitMs": 143,
            "userMs": 662,
            "profileAndPurposeMs": 129,
            "reservationMs": 396,
            "rateLimitMs": 131,
            "contextMs": 947,
            "contextCache": "miss",
            "aiVisibilityClaimContext": "not_requested",
            "contextWaitMs": 947,
            "phonicSessionMs": 914,
            "reservationUpdateMs": 65,
            "totalMs": 3488
        }
    }
    '''
    result = requests.post(
        'https://app.talentpluto.com/api/talent/voice/web-call',
        json={
            # Randomly generated UUID on the client's side.
            'reservationCallId': 'web-call-reservation:' + str(uuid.uuid4()),
        },
        cookies=cookies, headers=headers,
    ).json()

    if 'error' in result:
        print(result['error'])
        return

    now = time.time()
    with open(CALL_FILE, 'w') as f:
        f.write(str(now + result['expiresInSeconds']))
        f.write('\n')
        f.write(json.dumps(result))

    return result


def prewarm_call():
    '''
    Example:
    {
        "success": true,
        "timings": {
            "contextCache": "hit", | "miss",
            "contextMs": 1265,
            "totalMs": 1695
        }
    }
    '''
    return requests.post(
        'https://app.talentpluto.com/api/talent/voice/web-call/prewarm',
        cookies=cookies, headers=headers,
    ).json()


def stop_call(call_id: str):
    '''
    Example:
    {
        "stoppedCount":1,
        "success":true
    }
    '''
    return requests.post(
        'https://app.talentpluto.com/api/talent/voice/web-call/stop',
        json={'callId': call_id},
        cookies=cookies,
        headers=headers,
    )


class printer(rich.live.Live):
    def __init__(self, *a, **kwa) -> None:
        self.group: rich.console.Group = rich.console.Group()
        super().__init__(
            renderable=self.group, auto_refresh=False,
            vertical_overflow='visible',
            *a, **kwa,
        )

    def _new_markdown(self, style: str) -> None:
        md = rich.markdown.Markdown(markup='', style=style)
        self.group.renderables.append(md)

    def append_markdown(self, appended: str, style: str, force_new: bool = False) -> None:
        renderables = self.group.renderables
        if len(renderables) == 0:
            self._new_markdown(style)

        last_renderable = renderables[-1]
        assert isinstance(last_renderable, rich.markdown.Markdown)
        if force_new or style != last_renderable.style:
            self._new_markdown(style)

        last_renderable = renderables[-1]
        assert isinstance(last_renderable, rich.markdown.Markdown)
        renderables[-1] = last_renderable.__class__(
            markup=last_renderable.markup + appended,
            style=last_renderable.style,
        )

        self.update(renderable=self.group)
        self.refresh()


async def do_call(url: str, token: str):
    running = asyncio.Event()
    printer_obj = printer()
    printer_obj.start()

    room = livekit.rtc.Room()
    await room.connect(url, token)
    platform_audio = livekit.rtc.PlatformAudio()

    @room.on("track_unsubscribed")
    def on_track_subscribed(track: livekit.rtc.Track, *a):
        if isinstance(track, livekit.rtc.RemoteAudioTrack):
            running.set()

    @room.on("disconnected")
    def on_disconnected() -> None:
        running.set()

    @room.on("data_received")
    def on_data_received(data: livekit.rtc.DataPacket) -> None:
        json_data = json.loads(data.data)
        match json_data['type']:
            case 'transcript_chunk':
                printer_obj.append_markdown(
                    appended=json_data['text'], style='bold',
                )
            case 'input_text':
                printer_obj.append_markdown(
                    appended=json_data['text'], style='italic',
                )
            case 'tool_call_output_processed' | 'assistant_ended_conversation':
                printer_obj.append_markdown(
                    appended=f'\n```json\n{json.dumps(data)}\n```\n', style='',
                )

    # Uses the audio source to create a track and publish it.
    await room.local_participant.publish_track(
        track=livekit.rtc.LocalAudioTrack.create_audio_track(
            name="mic",
            source=platform_audio.create_audio_source(
                options=livekit.rtc.PlatformAudioOptions(
                    echo_cancellation=True,   # Acoustic Echo Cancellation
                    noise_suppression=True,   # Noise suppression
                )
            )
        ),
        options=livekit.rtc.TrackPublishOptions(
            source=livekit.rtc.TrackSource.SOURCE_MICROPHONE,
        ),
    )

    try:
        await running.wait()
    except Exception:
        pass
    finally:
        await room.disconnect()
        printer_obj.stop()


async def main():
    if not (prewarm_response := prewarm_call()):
        return
    if not (web_call_response := start_call()):
        return
    await do_call(
        url=web_call_response['url'],
        token=web_call_response['token'],
    )
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
