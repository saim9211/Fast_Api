from fastapi import FastAPI
app=FastAPI()
@app.get("/")
def fist_try():
    return {"message": "first impression is the last one"}
@app.get("/second_try")
def second_try():
    return {"message": "second impression is also important"}