from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/fenoma/1")
async def root():
    return {"message": "Endpoint  #1"}