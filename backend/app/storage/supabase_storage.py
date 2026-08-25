from app.core.supabase import supabase
import tempfile

class SupabaseStorage:

    BUCKET = "documents"

    async def upload(
        self,
        file,
        user_id: int,
        chatbot_id: int
    ):

        storage_path = (
            f"user_{user_id}/"
            f"chatbot_{chatbot_id}/"
            f"{file.filename}"
        )

        contents = await file.read()

        supabase.storage.from_(self.BUCKET).upload(
            path=storage_path,
            file=contents,
            file_options={
                "content-type": file.content_type,
                "upsert": "true"
            }
        )

        return storage_path, file.filename


    def download(self, storage_path):

        response = (
            supabase.storage
            .from_(self.BUCKET)
            .download(storage_path)
        )

        suffix = "." + storage_path.split(".")[-1]

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        )

        temp.write(response)

        temp.close()

        return temp.name

    def delete(self, storage_path: str):
        print(f"Deleting: {storage_path}")

        result = supabase.storage.from_(self.BUCKET).remove(
            [storage_path]
        )

        print(result)

supabase_storage = SupabaseStorage()