from fastapi import FastAPI
from app.api.routers import v1_router


app = FastAPI()


app.include_router(v1_router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="app.main:app", host="0.0.0.0", port=8100, reload=True)
