import os
from fastapi import UploadFile

from app.storage.base import StorageService


class LocalStorageService(StorageService):

    async def upload(
        self,
        file: UploadFile,
        user_id: int,
        chatbot_id: int
    ):

        upload_dir = (
            f"uploads/user_{user_id}/"
            f"chatbot_{chatbot_id}"
        )

        os.makedirs(
            upload_dir,
            exist_ok=True
        )

        file_path = os.path.join(
            upload_dir,
            file.filename
        )

        contents = await file.read()

        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        return (
            file_path,
            file.filename
        )

    def delete(
        self,
        file_path: str
    ):

        if os.path.exists(file_path):
            os.remove(file_path)

local_storage = LocalStorageService()