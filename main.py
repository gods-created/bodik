from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares import IfRouteNotFoundMiddleware
from routes import training_route, prediction_route
from uvicorn import run

app = FastAPI(
    title='Bodik API',
    description='',
    version='0.0.1',
    redoc_url=None,
    docs_url='/docs',
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_headers=['*'],
    allow_methods=['*'],
    allow_origins=['http://127.0.0.1', 'http://ec2-3-84-120-184.compute-1.amazonaws.com']
)

app.add_middleware(IfRouteNotFoundMiddleware)

app.include_router(training_route)
app.include_router(prediction_route)

if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8000, reload=True)