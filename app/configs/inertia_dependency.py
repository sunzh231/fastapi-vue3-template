
from fastapi.templating import Jinja2Templates
import os
from inertia import InertiaConfig, inertia_dependency_factory, Inertia
from fastapi import Depends
from typing import Annotated

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
