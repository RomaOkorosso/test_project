from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import auth, user, post

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)


@app.route("/", methods=["GET"])
async def index(_):
    return HTMLResponse(
        "<div style='text-align: center;'>"
        f"<a style='font-size: 64px' href='http://localhost:{settings.APP_PORT}/redoc'>re-doc</a>"
        " <br> "
        f"<a style='font-size: 64px' href='http://localhost:{settings.APP_PORT}/docs'>swagger</a>"
        "</div>"
    )


@app.get("/openapi.json")
async def openapi():
    return get_openapi(
        title="Test task",
        version="1.0.0",
        routes=app.routes,
    )
