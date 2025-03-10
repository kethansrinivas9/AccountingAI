import uvicorn
from fastapi import FastAPI
from fastapi import APIRouter
from routers import document

app = FastAPI(title="Accounting AI App")

# Include document processing endpoints
app.include_router(document.router)

@app.get("/")
def root():
    return {"message": "Welcome to AI DocFlow"}


if __name__ == '__main__':
    uvicorn.run(app=app,
                host='0.0.0.0',
                port=8080
                )