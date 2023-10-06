from transformers import GPT2LMHeadModel, GPT2Tokenizer

from logger import get_logger
from rugpt3.settings import GPT3ControllerSettings

logger = get_logger(__name__)


class GPT3Controller:
    def __init__(self, settings: GPT3ControllerSettings):
        self._settings = settings

    def _generate(self, request_text: str) -> str:
        tokenizer = GPT2Tokenizer.from_pretrained(self._settings.name_or_path_model)
        model = GPT2LMHeadModel.from_pretrained(self._settings.name_or_path_model)
        input_ids = tokenizer.encode(
            request_text, return_tensors=self._settings.return_tensors
        )
        out = model.generate(
            input_ids,
            top_k=self._settings.top_k,
            top_p=self._settings.top_p,
            num_beams=self._settings.num_beams,
            num_return_sequences=self._settings.num_return_sequences,
            do_sample=self._settings.do_sample,
            no_repeat_ngram_size=self._settings.no_repeat_ngram_size,
            temperature=self._settings.temperature,
            repetition_penalty=self._settings.repetition_penalty,
            length_penalty=self._settings.length_penalty,
            eos_token_id=self._settings.eos_token_id,
            max_new_tokens=self._settings.max_new_tokens,
        )
        text = list(map(tokenizer.decode, out))[0][len(request_text) :]
        logger.debug("Row generate text '%s'", text)
        if (answer_end := text.find("@@ПЕРВЫЙ@@")) > -1:
            text = text[: answer_end - 1]
        logger.info("Generate text '%s'", text)
        return text

    def question(self, question_text: str) -> str:
        text = (
            self._settings.question_begin + question_text + self._settings.answer_begin
        )
        logger.info("Start generate answer for question '%s'", text)
        return self._generate(text)
