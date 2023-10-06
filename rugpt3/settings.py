from pydantic_settings import BaseSettings


class GPT3ControllerSettings(BaseSettings):
    name_or_path_model: str = "tinkoff-ai/ruDialoGPT-medium"
    return_tensors: str = "pt"
    question_begin: str = "@@ПЕРВЫЙ@@ "
    answer_begin: str = " @@ВТОРОЙ@@"
    top_k: int = 10
    top_p: float = 0.95
    num_beams: int = 3
    num_return_sequences: int = 3
    do_sample: bool = True
    no_repeat_ngram_size: int = 2
    temperature: float = 1.2
    repetition_penalty: float = 1.2
    length_penalty: float = 1.0
    eos_token_id: int = 50257
    max_new_tokens: int = 25

    class Config:
        env_prefix = "GPT3_CONTROLLER_"
