import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from starlette.middleware.authentication import AuthenticationMiddleware

MODELS = ["app.users.model", "app.reading.model"]

Tortoise.init_models(
    MODELS,
    "models",
)


from .math import router as math_router
from .writing import router as writing_router
# from .reading import router as reading_router


tags_metadata = [
    {"name": "Math", "description": "math"},
    # {"name": "Reading", "description": "reading"},
    {"name": "Writing", "description": "writing"},
]


app = FastAPI(title="SAT Problem Generator", openapi_tags=tags_metadata)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())

app.include_router(math_router.router)
app.include_router(writing_router.router)
# app.include_router(reading_router.router)

register_tortoise(
    app,
    db_url="sqlite://db/db.sqlite3",
    modules={"models": MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
