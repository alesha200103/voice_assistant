from pydantic_settings import BaseSettings


class TTSSettings(BaseSettings):
    device: str = "cpu"
    num_threads: int = 2
    file_path_model: str = "model.pt"
    url_model: str = "https://models.silero.ai/models/tts/ru/v4_ru.pt"
    name_model: str = "tts_models"
    type_model: str = "model"
    sample_rate: int = 24000  # 8000, 24000, 4800
    speaker: str = "aidar"  # aidar, baya, kseniya, xenia, eugene, random

    class Config:
        env_prefix = "TTS_"
