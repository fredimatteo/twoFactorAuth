from fastapi import FastAPI

app = FastAPI(
    title="two factor API",
    description="API for two factor authentication",
    version="0.0.1",

)


@app.get("/")
def root():
    return {"message": "Hello coder!"}
