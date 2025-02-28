from typing import TypedDict


class CloudStorageDataDict(TypedDict):
    bucket: str = ""
    path: str = ""
    url: str = ""
