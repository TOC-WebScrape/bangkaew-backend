import uvicorn
from app import app

if __name__ == "__main__":
    uvicorn.run("app.app:App", host="172.0.0.1", port=5000, reload=True)
