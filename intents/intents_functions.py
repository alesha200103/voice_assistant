from random import choice

from intents.settings import Actions, IntentsFunctionsSettings
from logger import get_logger
from tts import TTS

logger = get_logger(__name__)


class IntentsFunctions:
    def __init__(self, tts: TTS, settings: IntentsFunctionsSettings) -> None:
        logger.info("Init IntentsFunctions")
        self._tts = tts
        self._settings = settings
        logger.info("IntentsFunctions successfully init")

    def play_greetings(self) -> Actions:
        logger.info("Start intent function play_greetings")
        greeting_phrase = choice(self._settings.greetings)
        self._tts.sey(greeting_phrase)
        return Actions.CONTINUE

    def play_farewell(self) -> Actions:
        logger.info("Start intent function play_farewell")
        farewell_phrase = choice(self._settings.farewell)
        self._tts.sey(farewell_phrase)
        return Actions.BREAK

    def tolk_with_bot(self) -> Actions:
        return Actions.TALK_WITH_BOT

    def start_intent_func(self, intent_fun_name: str) -> Actions:
        logger.info("Finding intent function")
        if intent_fun_name == self.play_greetings.__name__:
            return self.play_greetings()
        if intent_fun_name == self.play_farewell.__name__:
            return self.play_farewell()
        if intent_fun_name == self.tolk_with_bot.__name__:
            return self.tolk_with_bot()
        return Actions.NO_ACTION
