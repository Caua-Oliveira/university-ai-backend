import io
from pathlib import Path
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import uuid


STATIC_DIR = Path(__file__).parent.parent.parent / "static" / "audios"
STATIC_DIR.mkdir(exist_ok=True, parents=True)

rec = sr.Recognizer()

async def speech_to_text(audio_bytes: bytes) -> str:
    """
    Converte áudio em texto usando a API do Google Speech Recognition.
    """

    try:
        # Carrega o áudio qualquer
        input_audio = io.BytesIO(audio_bytes)
        audio_segment = AudioSegment.from_file(input_audio)


        # Exporta o áudio para WAV em memória
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        # Manda o WAV para o STT
        with sr.AudioFile(wav_io) as source:
            audio_data = rec.record(source)

        text = rec.recognize_google(audio_data, language='pt-BR')
        return text

    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print(f"Falha no reconhecimento de voz: {e}")
        return ""


async def text_to_speech(text: str, user_id: str = "default_user") -> str:
    try:
        filename = f"{uuid.uuid4()}.mp3"
        filepath = STATIC_DIR / filename

        tts = gTTS(text=text, lang='pt', tld='com.br')
        tts.save(str(filepath))

        return f"/static/audios/{filename}"
    except Exception as e:
        print(f"Erro na conversão de texto para fala: {e}")
        return ""