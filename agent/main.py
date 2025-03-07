from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Agent FastAPI is running!"}

@app.get("/process")
def process_data():
    return {"response": f"Processed"}
