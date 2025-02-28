import os
from time import time

# Imports the Google Cloud client library
from google.cloud import storage

from app.storage.storage_models import CloudStorageDataDict

# Instantiates a client
storage_client = storage.Client()


def upload_bytes_to_ref_0(path: str, file: bytes) -> CloudStorageDataDict:
    bucket_name = os.getenv("DEFAULT_BUCKET")
    # bucket_name = f"{project_id}.appspot.com"
    bucket = storage_client.get_bucket(bucket_name)

    blob = bucket.blob(path)
    blob.upload_from_string(file)
    blob.make_public()
    print("Debió terminar la carga", blob)
    result = {"bucket": bucket_name, "path": blob.name, "url": blob.public_url}
    return result


def upload_bytes_to_ref(path: str, file: bytes, metadata: dict | None = None) -> CloudStorageDataDict:
    bucket_name = os.getenv("DEFAULT_BUCKET")
    bucket = storage_client.get_bucket(bucket_name)

    # bucket_name = f"{environment.project_id}.appspot.com"
    # bucket = storage_client.get_bucket(bucket_name)

    blob = bucket.blob(path)
    if metadata:
        blob.metadata = metadata

    blob.upload_from_string(file)
    blob.make_public()
    print("Debió terminar la carga", blob)
    return CloudStorageDataDict(bucket=bucket_name, path=blob.name, url=blob.public_url)


def get_storage_path(lang: str, entity_path: str, entity_id: str, file_type: str, file_name: str, extension: str | None = None) -> str:  # noqa: PLR0913
    file_name = file_name.replace(" ", "")[:20]
    now = int(time())
    file_name = f"{file_name}_{now}"
    # if len(file_name) > 20:
    #     file_name = file_name[:20]
    # es/words/lexeme/audios/lexeme.mp3
    # es/words/learningExamples/abcd1234/audios/a_learning_exapple.mp3
    path = f"{lang}/{entity_path}/{entity_id}/{file_type}/{file_name}"

    if extension:
        path += f".{extension}"

    return path
