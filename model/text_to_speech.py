import os, requests, time
import pyaudio
import wave


class TextToSpeech():
    def __init__(self, subscription_key, text):
        self.subscription_key = subscription_key
        # self.tts = input("What would you like to convert to speech: ")
        self.tts = text
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None
        self.filename = ""

    def get_token(self):
        fetch_token_url = (
            "https://westus2.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        )
        headers = {"Ocp-Apim-Subscription-Key": self.subscription_key}
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def play_audio(self):
        # define stream chunk
        chunk = 1024

        # open a wav format music

        # dir_path = os.path.abspath(os.path.dirname(__file__))
        # file_path = os.path.join(dir_path, "sounds/", self.filename)
        ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(ROOT_DIR, "sounds/", self.filename)

        f = wave.open(file_path, "rb")
        # instantiate PyAudio
        p = pyaudio.PyAudio()
        # open stream
        stream = p.open(
            format=p.get_format_from_width(f.getsampwidth()),
            channels=f.getnchannels(),
            rate=f.getframerate(),
            output=True,
        )
        # read data
        data = f.readframes(chunk)

        # play stream
        while data:
            stream.write(data)
            data = f.readframes(chunk)

        # stop stream
        stream.stop_stream()
        stream.close()

        # close PyAudio
        p.terminate()
        pass

    def save_audio(self):
        base_url = "https://westus2.tts.speech.microsoft.com/"
        path = "cognitiveservices/v1"
        constructed_url = base_url + path
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
            "User-Agent": "corgi",
            "cache-control": "no-cache",
        }
        body = (
            "<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Female' name='Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'>"
            + self.tts
            + "</voice></speak>"
        )

        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            self.filename = "sample-" + self.timestr + ".wav"

            # dir_path = os.path.abspath(os.path.dirname(__file__))
            ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(ROOT_DIR, "sounds/", self.filename)
            try:
                with open(file_path, "wb") as audio:
                    audio.write(response.content)
                    print(
                        "\nStatus code: "
                        + str(response.status_code)
                        + "\nYour TTS is ready for playback.\n"
                    )
            except:
                print("file open error!")
        else:
            print(
                "\nStatus code: "
                + str(response.status_code)
                + "\nSomething went wrong. Check your subscription key and headers.\n"
            )


if __name__ == "__main__":
    subscription_key = "2c14b0315f804a17a54fae4be07dd2a3"
    app = TextToSpeech(subscription_key, "test")
    app.get_token()
    app.save_audio()
    app.play_audio()
