from typing_extensions import TypedDict


class IObject(TypedDict, total=False):
    id: int
    name: str
    target_image_file: str
    asset_file: str
    subzone_id: int
