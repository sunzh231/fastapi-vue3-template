from typing import Union
import os

from fastapi import Depends
from typing import Annotated
from inertia import InertiaConfig, inertia_dependency_factory, Inertia
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from inertia import InertiaResponse, InertiaVersionConflictException, inertia_version_conflict_exception_handler
# from inertia_dependency import InertiaDependency
from starlette.middleware.sessions import SessionMiddleware
import secrets

app = FastAPI()

# 添加 SessionMiddleware，使用随机密钥
app.add_middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(32))

templates = Jinja2Templates(directory="templates")


manifest_json = os.path.join(
    os.path.dirname(__file__), "dist", "manifest.json"
)
inertia_config = InertiaConfig(
    templates=templates,
    manifest_json_path=manifest_json,
    environment="development",
    use_flash_messages=True,
    use_flash_errors=True,
    entrypoint_filename="main.js",
    root_directory="frontend",
)
InertiaDep = Annotated[Inertia, Depends(inertia_dependency_factory(inertia_config))]

# 直接挂载templates目录，这样/templates/assets和/templates/vite.svg都能被正确访问
# app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
app.mount("/assets", StaticFiles(directory=os.path.join(os.path.join(os.path.dirname(__file__), "dist"), "assets")), name="assets")

app.add_exception_handler(InertiaVersionConflictException, inertia_version_conflict_exception_handler)

@app.get('/', response_model=None)
async def index(inertia: InertiaDep) -> InertiaResponse:
    return await inertia.render('Index', {
        'name': 'John Doe'
    })

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
