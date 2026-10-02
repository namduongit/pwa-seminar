from typing import Annotated

from core.provider.mongo import get_mongo
from fastapi import Depends
from pymongo.asynchronous.database import AsyncDatabase

MongoDB = Annotated[AsyncDatabase, Depends(get_mongo)]
