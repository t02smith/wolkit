import uvicorn
import router.router
import router.advice
from router.app import app


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5055, reload=True)
