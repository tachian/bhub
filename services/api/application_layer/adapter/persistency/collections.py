from typing import NamedTuple, Sequence, Union


class Collection(NamedTuple):
    name: str
    validator: dict
    index: Union[
        str, Sequence[tuple]
    ]  # A sequence will be interpreted as one compound index
    unique_index: bool


collections_definitions = [
    Collection(
        "Payments",
        validator={
            "bsonType": "object",
            "required": ["uuid"],
            "properties": {
                "uuid": {
                    "bsonType": "string",
                    "description": "must be a string and is required",
                }
            },
        },
        index="uuid",
        unique_index=True,
    ),
]
