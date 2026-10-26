from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def proba():
    return {"message": "Moj projekat"}