from abc import ABC, abstractmethod
from fastapi import UploadFile


class StorageService(ABC):

    @abstractmethod
    async def upload(
        self,
        file: UploadFile,
        user_id: int,
        chatbot_id: int
    ) -> tuple[str, str]:
        """
        Returns:
            file_path,
            file_name
        """
        pass

    @abstractmethod
    def delete(
        self,
        file_path: str
    ):
        pass