import os
import warnings

import torch
from pydub import AudioSegment
from pydub.playback import play

from logger import get_logger
from tts.settings import TTSSettings

logger = get_logger(__name__)

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)


class TTS:
    def __init__(self, settings: TTSSettings) -> None:
        logger.info("Start init TTS")
        self._settings = settings
        self._device = torch.device(self._settings.device)
        torch.set_num_threads(self._settings.num_threads)
        if not os.path.isfile(self._settings.file_path_model):
            logger.info("Download model")
            torch.hub.download_url_to_file(
                self._settings.url_model, self._settings.file_path_model
            )

        self._model = torch.package.PackageImporter(
            self._settings.file_path_model
        ).load_pickle(self._settings.name_model, self._settings.type_model)
        self._model.to(self._device)
        self._sample_rate = self._settings.sample_rate
        self._speaker = self._settings.speaker
        logger.info("Model init successful")

    def sey(self, text: str) -> None:
        logger.info("Start saying '%s'", text)
        audio_paths = self._model.save_wav(  # apply_tts
            text=text, speaker=self._speaker, sample_rate=self._sample_rate
        )  # костыль с созданием файла
        # import tensorflow as tf
        # print(tf.io.serialize_tensor(audio_paths))
        audio = AudioSegment.from_wav(audio_paths)
        play(audio)
        os.remove(audio_paths)
        logger.info("Successful say")
