from app import app
from app.configs.inertia_dependency import InertiaDep
from inertia import InertiaResponse

@app.get('/', response_model=None)
async def index(inertia: InertiaDep) -> InertiaResponse:
    return await inertia.render('Index', {
        'name': 'John Doe'
    })
