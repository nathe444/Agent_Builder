from abc import ABC, abstractmethod
from typing import Iterator


class BaseLLMProvider(ABC):

    @abstractmethod
    def chat(
        self,
        messages: list[dict]
    ) -> str:
        pass

    @abstractmethod
    def chat_stream(
        self,
        messages: list[dict]
    ) -> Iterator[str]:
        pass