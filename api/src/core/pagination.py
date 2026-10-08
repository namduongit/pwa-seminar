from pydantic import BaseModel


class Pagination[T](BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    data: list[T]


def lookup_one(
    collection: str, local_field: str, foreign_field: str, alias: str
) -> list[dict]:
    return [
        {
            "$lookup": {
                "from": collection,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": alias,
            }
        },
        {"$set": {alias: {"$first": f"${alias}"}}},
    ]


def lookup_many(
    collection: str, local_field: str, foreign_field: str, alias: str
) -> dict:
    return {
        "$lookup": {
            "from": collection,
            "localField": local_field,
            "foreignField": foreign_field,
            "as": alias,
        }
    }
