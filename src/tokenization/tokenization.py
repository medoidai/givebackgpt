from typing import List

import tiktoken

def preload_model_encodings(models: List[str]) -> None:
    for model in models:
        tiktoken.encoding_for_model(model)

def truncate_text_from_end(text: str, max_n_tokens: int, model: str) -> str:
    encoding = tiktoken.encoding_for_model(model)

    text_tokens = encoding.encode(text, allowed_special="all")

    if len(text_tokens) <= max_n_tokens:
        return text

    truncated_tokens = text_tokens[:max_n_tokens]

    truncated_text = encoding.decode(truncated_tokens)

    return truncated_text

def truncate_text_from_middle(text: str, max_n_tokens: int, model: str) -> str:
    encoding = tiktoken.encoding_for_model(model)

    text_tokens = encoding.encode(text, allowed_special="all")

    if len(text_tokens) <= max_n_tokens:
        return text

    separator_text = " ... "

    separator_tokens = encoding.encode(separator_text)

    safety_margin_n_tokens = 20

    remaining_n_tokens = max_n_tokens - len(separator_tokens) - safety_margin_n_tokens

    if remaining_n_tokens < 2:
        return encoding.decode(text_tokens[:max_n_tokens])

    keep_start = remaining_n_tokens // 2

    keep_end = remaining_n_tokens - keep_start

    truncated_tokens = text_tokens[:keep_start] + separator_tokens + text_tokens[-keep_end:]

    return encoding.decode(truncated_tokens)