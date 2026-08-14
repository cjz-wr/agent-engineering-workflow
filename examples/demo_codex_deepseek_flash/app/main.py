"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .config import settings
from .db import init_db
from .templating import render_page

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

from .routes import auth as auth_routes  # noqa: E402
from .routes import admin as admin_routes  # noqa: E402
from .routes import comments as comments_routes  # noqa: E402
from .routes import public as public_routes  # noqa: E402
from .routes import posts as posts_routes  # noqa: E402

app.include_router(auth_routes.router)
app.include_router(admin_routes.router)
app.include_router(comments_routes.router)
app.include_router(posts_routes.router)
app.include_router(public_routes.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Preserve redirect headers (Location / HX-Redirect) used by auth guards.
    if exc.headers:
        return JSONResponse(
            {"detail": exc.detail}, status_code=exc.status_code, headers=exc.headers
        )
    if exc.status_code == 404 and "text/html" in request.headers.get("accept", ""):
        return render_page(request, "404.html", status_code=404)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
