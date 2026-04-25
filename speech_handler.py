"""
Speech handler — Text-to-Speech and Speech-to-Text utilities.

TTS:  gTTS (free) with optional ElevenLabs upgrade
STT:  Deepgram (via API) with Whisper fallback (local)

In the Twilio voice flow, Twilio handles most of the STT natively
using its <Gather speech> feature. These helpers are available for
any custom audio processing needs outside of the live call flow.
"""

import os
import logging
import tempfile
import hashlib

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# TEXT-TO-SPEECH
# ──────────────────────────────────────────────────────────────────────────────

def text_to_speech_file(text: str, language: str = "en") -> str:
    """
    Convert text to an MP3 file using gTTS.
    Returns the path to the generated file.
    Caches based on text hash to avoid re-generating.
    """
    try:
        from gtts import gTTS

        lang_map = {
            "en": "en", "hi": "hi", "kn": "kn",
            "mr": "mr", "te": "te"
        }
        tts_lang = lang_map.get(language, "en")

        # Cache key from text + language
        cache_key = hashlib.md5(f"{text}{tts_lang}".encode()).hexdigest()
        cache_dir = "/tmp/voicebot_tts"
        os.makedirs(cache_dir, exist_ok=True)
        cache_path = os.path.join(cache_dir, f"{cache_key}.mp3")

        if not os.path.exists(cache_path):
            tts = gTTS(text=text, lang=tts_lang, slow=False)
            tts.save(cache_path)
            logger.info(f"🔊 TTS generated: {cache_path}")
        else:
            logger.info(f"🔊 TTS cache hit: {cache_path}")

        return cache_path

    except ImportError:
        logger.error("gTTS not installed. Run: pip install gTTS")
        raise
    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise


def text_to_speech_url(text: str, language: str = "en", base_url: str = "") -> str:
    """
    Generate TTS audio and return a publicly accessible URL.
    In production, upload to S3/GCS and return the URL.
    For local dev, serves the file via FastAPI /audio endpoint.
    """
    # For demo: Twilio uses its own TTS via <Say>, so this is a placeholder
    # In production: upload to cloud storage, return URL
    return f"{base_url}/audio?text={text}&lang={language}"


# ──────────────────────────────────────────────────────────────────────────────
# SPEECH-TO-TEXT  (used for non-Twilio audio processing)
# ──────────────────────────────────────────────────────────────────────────────

def transcribe_audio(audio_file_path: str, language: str = "en") -> str:
    """
    Transcribe an audio file using Deepgram (preferred) or Whisper (fallback).
    
    NOTE: In the live call flow, Twilio's <Gather> handles STT automatically
    and passes `SpeechResult` to our webhook. This function is for processing
    recordings or uploaded audio separately.
    """
    deepgram_key = os.getenv("DEEPGRAM_API_KEY")

    if deepgram_key:
        return _transcribe_deepgram(audio_file_path, language, deepgram_key)
    else:
        logger.warning("DEEPGRAM_API_KEY not set, falling back to Whisper")
        return _transcribe_whisper(audio_file_path)


def _transcribe_deepgram(audio_path: str, language: str, api_key: str) -> str:
    """Transcribe using Deepgram API."""
    try:
        import httpx

        lang_map = {"en": "en-US", "hi": "hi", "kn": "kn", "mr": "mr", "te": "te"}
        dg_lang = lang_map.get(language, "en-US")

        with open(audio_path, "rb") as f:
            audio_data = f.read()

        response = httpx.post(
            f"https://api.deepgram.com/v1/listen?language={dg_lang}&model=general",
            headers={
                "Authorization": f"Token {api_key}",
                "Content-Type": "audio/wav",
            },
            content=audio_data,
            timeout=30.0,
        )
        result = response.json()
        transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]
        logger.info(f"🎙️ Deepgram transcript: '{transcript}'")
        return transcript

    except Exception as e:
        logger.error(f"Deepgram STT error: {e}")
        return ""


def _transcribe_whisper(audio_path: str) -> str:
    """Transcribe using OpenAI Whisper (local model)."""
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        transcript = result.get("text", "")
        logger.info(f"🎙️ Whisper transcript: '{transcript}'")
        return transcript
    except ImportError:
        logger.error("Whisper not installed. Run: pip install openai-whisper")
        return ""
    except Exception as e:
        logger.error(f"Whisper STT error: {e}")
        return ""
