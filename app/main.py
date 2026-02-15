from fastapi import FastAPI
from pydantic import BaseModel
from app.router import process_query

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_handler(request: QueryRequest):
    response = process_query(request.query)
    return {"response": response}
