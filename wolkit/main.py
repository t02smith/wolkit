import uvicorn
from db.setup import setup_db
import logging


if __name__ == "__main__":
    setup_db()
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run("router.app:app", host="127.0.0.1", port=5055, reload=True)
