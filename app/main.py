import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.app:App", port=5000, reload=True)
