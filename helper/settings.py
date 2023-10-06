from pydantic_settings import BaseSettings


class HelperSettings(BaseSettings):
    activate_phrase: set[str] = {
        "слушай акакий",
        "акакий слушай",
        "послушай акакий",
        "акакий послушай",
    }  # сет активирующих начало деалога фраз
    background_energy_threshold: int = 1000
    background_dynamic_energy_threshold: bool = False
    energy_threshold: int = 300
    dynamic_energy_threshold: bool = True
    default_language: str = "ru"
    continue_speech_time: int = 5  # время больше которого реч не распознаётся
    is_offline: bool = False  # False

    class Config:
        env_prefix = "HELPER_"
