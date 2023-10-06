import json

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from intents.intents_functions import IntentsFunctions
from intents.settings import Actions, IntentControllerSettings
from logger import get_logger

logger = get_logger(__name__)


class IntentController:
    def __init__(
        self,
        vectorizer: CountVectorizer,
        classifier_probability: LogisticRegression,
        classifier: LinearSVC,
        intents_functions: IntentsFunctions,
        settings: IntentControllerSettings,
    ):
        logger.info("Start init intent controller")
        self._settings = settings
        self._classifier_probability = classifier_probability
        self._classifier = classifier
        self._vectorizer = vectorizer
        self._intents_functions = intents_functions

        with open(self._settings.config_intents_path, encoding="utf-8") as intents:
            self._config_intents = json.load(intents)

        corpus = []
        target_vector = []
        for intent_name, intent_data in self._config_intents["intents"].items():
            for example in intent_data["examples"]:
                corpus.append(example)
                target_vector.append(intent_name)

        self._training_vector = vectorizer.fit_transform(corpus)  # TfidfVectorizer
        self._classifier_probability.fit(self._training_vector, target_vector)
        self._classifier.fit(self._training_vector, target_vector)
        logger.info("Intent controller successfully init")

    def get_intent(self, request: str) -> str:
        logger.info("Get intent")
        best_intent = self._classifier.predict(self._vectorizer.transform([request]))[0]

        index_of_best_intent = list(self._classifier_probability.classes_).index(
            best_intent
        )
        probabilities = self._classifier_probability.predict_proba(
            self._vectorizer.transform([request])
        )[0]

        best_intent_probability = probabilities[index_of_best_intent]

        if best_intent_probability > self._settings.min_best_intent_probability:
            logger.info(
                "Get intent '%s' with probability %s",
                best_intent,
                best_intent_probability,
            )
            return best_intent
        logger.info("No intent")
        return self._settings.no_intent

    def start_intent(self, intent: str) -> Actions:
        logger.info("Starting intent '%s'", intent)
        if intent == self._settings.no_intent:
            logger.info("No intent, skip")
            return Actions.NO_ACTION

        intent_function_name = self._config_intents["intents"][intent].get("responses")
        if intent_function_name is None:
            logger.info("No function for intent '%s'", intent)
            return Actions.NO_ACTION

        return self._intents_functions.start_intent_func(intent_function_name)
