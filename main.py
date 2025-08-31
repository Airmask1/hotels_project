from fastapi import FastAPI

from hotels import router as router_hotels

app = FastAPI()

app.include_router(router=router_hotels, tags=["Отели"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
