import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import document

app = FastAPI(title="Accounting AI App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include document processing endpoints
app.include_router(document.router)

@app.get("/")
def root():
    return {"message": "Welcome to AI DocFlow"}


if __name__ == '__main__':
    uvicorn.run(app=app,
                host='0.0.0.0',
                port=8000
                )