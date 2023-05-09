import uvicorn
import router.router
import router.advice


if __name__ == "__main__":
    uvicorn.run("router.app:app", host="127.0.0.1", port=5055, reload=True)
