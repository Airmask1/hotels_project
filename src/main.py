import sys
from pathlib import Path

from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotels

app = FastAPI()

app.include_router(router=router_hotels, tags=["Отели"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
