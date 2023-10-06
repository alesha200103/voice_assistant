import typer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from speech_recognition import Microphone, Recognizer

from helper import Helper, HelperSettings
from intents import (Actions, IntentController, IntentControllerSettings,
                     IntentsFunctions, IntentsFunctionsSettings)
from rugpt3 import GPT3Controller, GPT3ControllerSettings
from tts import TTS, TTSSettings

helper_app = typer.Typer()


def get_tts() -> TTS:
    tts_settings = TTSSettings()
    return TTS(tts_settings)


def get_gpt3_controller() -> GPT3Controller:
    gpt3_controller_settings = GPT3ControllerSettings()
    return GPT3Controller(settings=gpt3_controller_settings)


def get_intent_controller(tts: TTS) -> IntentController:
    vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 3))
    classifier_probability = LogisticRegression()
    classifier = LinearSVC()
    intent_controller_settings = IntentControllerSettings()
    intents_functions_settings = IntentsFunctionsSettings()
    intents_functions = IntentsFunctions(tts=tts, settings=intents_functions_settings)
    return IntentController(
        vectorizer=vectorizer,
        classifier_probability=classifier_probability,
        classifier=classifier,
        settings=intent_controller_settings,
        intents_functions=intents_functions,
    )


def get_helper() -> Helper:
    rec = Recognizer()
    mic = Microphone()
    helper_settings = HelperSettings()
    return Helper(recognizer=rec, microphone=mic, settings=helper_settings)


@helper_app.command()
def run():
    #  TTS
    tts = get_tts()

    #  GPT3
    gpt3_controller = get_gpt3_controller()

    #  Intents
    intent_controller = get_intent_controller(tts=tts)

    #  Helper
    helper = get_helper()

    # main loop

    while True:
        helper.background_listen()

        tts.sey("Я вас вним+ательно сл+ушаю!")

        while (text_request := helper.listen()) is not None:
            intent = intent_controller.get_intent(text_request)

            match intent_controller.start_intent(intent):
                case Actions.CONTINUE:
                    continue
                case Actions.BREAK:
                    break
                case Actions.TALK_WITH_BOT:
                    talk_with_bot(
                        intent_controller=intent_controller,
                        gpt3_controller=gpt3_controller,
                        text_request=text_request,
                        tts=tts,
                        helper=helper,
                    )
                    continue

            answer_text = gpt3_controller.question(text_request)

            tts.sey(answer_text)


def talk_with_bot(
    intent_controller: IntentController,
    gpt3_controller: GPT3Controller,
    text_request: str,
    tts: TTS,
    helper: Helper,
) -> None:
    context: list[str] = [text_request]
    answer_text = gpt3_controller.question("".join(context))
    context.append("@@ВТОРОЙ@@ " + answer_text)
    tts.sey(answer_text)

    while (text_request := helper.listen()) is not None:
        intent = intent_controller.get_intent(text_request)

        if intent == "farewell":
            return None

        context.append("@@ПЕРВЫЙ@@ " + text_request)
        answer_text = gpt3_controller.question(" ".join(context))
        context.append("@@ВТОРОЙ@@ " + answer_text)
        tts.sey(answer_text)

        if len(context) > 6:
            context = context[-6:]


if __name__ == "__main__":
    helper_app()
