from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def chat(
        self,
        messages: list[dict]
    ) -> str:
        pass