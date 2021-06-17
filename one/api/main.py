from typing import Optional
from pydantic import BaseModel
from pydantic.types import UUID4
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy_utils as su


from app.settings import APP_HOST, APP_PORT, DEBUG
from app.routes.routes_utils import root, dev, admin
from app.routes.routes_users import user
from app.routes.routes_hobby import hobby
from app.routes.routes_helper import helper
from app.routes.routes_story import story
from app.models.base import db, DATABASE_URI
from app.utils.utils import upgrade_migrate_db
from app.utils.dependesies import get_data

app = FastAPI(title="""REST Api using FastAPI development app PRAQTIQA""")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(root)
app.include_router(story)
app.include_router(user)
app.include_router(hobby)
app.include_router(helper)
app.include_router(admin)
app.include_router(dev)


@app.on_event("startup")
async def open_db():
    await db.connect()


@app.on_event("shutdown")
async def close_db():
    await db.disconnect()

   


if __name__ == "__main__":
    uvicorn.run('main:app', host=APP_HOST,
                port=APP_PORT, workers=4,
                log_level="info", debug=DEBUG)
