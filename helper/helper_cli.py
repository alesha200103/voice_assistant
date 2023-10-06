from time import time

from speech_recognition import AudioData, Microphone, Recognizer
from speech_recognition.exceptions import UnknownValueError, WaitTimeoutError

from helper.settings import HelperSettings
from logger import get_logger

logger = get_logger(__name__)


class Helper:
    def __init__(
        self, recognizer: Recognizer, microphone: Microphone, settings: HelperSettings
    ) -> None:
        self._recognizer = recognizer
        self._microphone = microphone
        self._settings = settings

    def _recognize(self, recorded_data: AudioData) -> str:
        if self._settings.is_offline:
            logger.info("Start recognizing offline with whisper")
            return self._recognizer.recognize_whisper(
                audio_data=recorded_data,
                language=self._settings.default_language,
            )
        logger.info("Start recognizing online with Google")
        return self._recognizer.recognize_google(
            audio_data=recorded_data,
            language=self._settings.default_language,
        )

    def background_listen(self) -> None:
        self._recognizer.energy_threshold = self._settings.background_energy_threshold
        self._recognizer.dynamic_energy_threshold = (
            self._settings.background_dynamic_energy_threshold
        )

        while True:
            logger.info("Start listen in background")

            try:
                with self._microphone as source:
                    start_time = time()
                    recorded_data = self._recognizer.listen(source=source, timeout=3.5)
                    if (
                        delta_time := time() - start_time
                        > self._settings.continue_speech_time
                    ):
                        logger.info(
                            "Very long speech %s, skip it and continue listen",
                            delta_time,
                        )
                        continue
            except WaitTimeoutError:
                logger.info("Did not hear anything, continue listen")
                continue

            logger.info("End listen in background")
            try:
                rec_phrase = str(
                    self._recognize(
                        recorded_data=recorded_data,
                    )
                )
                logger.info("Recognized phrase '%s'", rec_phrase)
            except UnknownValueError:
                logger.info("Did not recognize anything, continue listen")
                continue

            if (
                activating_phrase := rec_phrase.lower()
            ) in self._settings.activate_phrase:
                logger.info(
                    "Get activating phrase '%s', listen carefully", activating_phrase
                )
                break

    def listen(self) -> None | str:
        self._recognizer.energy_threshold = self._settings.energy_threshold
        self._recognizer.dynamic_energy_threshold = (
            self._settings.dynamic_energy_threshold
        )

        logger.info("Start listen")

        try:
            with self._microphone as source:
                recorded_data = self._recognizer.listen(source=source, timeout=30)
        except WaitTimeoutError:
            logger.info("Did not hear anything")
            return

        logger.info("End listen")
        try:
            rec_phrase = str(
                self._recognize(
                    recorded_data=recorded_data,
                )
            )
            logger.info("Recognized phrase '%s'", rec_phrase)
        except UnknownValueError:
            logger.info("Did not recognize anything")
            return

        return rec_phrase
