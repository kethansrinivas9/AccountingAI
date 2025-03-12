from fastapi import APIRouter, UploadFile, File, Query, Depends
from langchain.chains import RetrievalQA
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.helpers.db_helper import extract_and_store_document_embeddings, \
    extract_closest_documents_based_on_embeddings
from backend.helpers.s3_helper import upload_file_to_s3, get_s3_content_from_uri

# OpenAI Embeddings
embeddings_model = OpenAIEmbeddings()

router = APIRouter(prefix="/documents", tags=["Documents"])



@router.post("/upload/")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Uploads document to S3 and processes it using AI"""
    file_path = f"uploads/{file.filename}"
    print("file path is: " + file_path)

    file_content = await file.read()

    s3_url = await upload_file_to_s3(file, file_content, file_path)
    await extract_and_store_document_embeddings(file_content, file.filename, s3_url, db)

    return {"message": "File uploaded successfully", "filename": file.filename}


@router.get("/query/")
async def query_document(question: str = Query(...), db: Session = Depends(get_db)):
    """Fetch relevant documents from Neon PostgreSQL using vector search and generate AI response."""

    query_embedding = await embeddings_model.aembed_query(question)  # Async call

    documents = await extract_closest_documents_based_on_embeddings(query_embedding, db)

    # Handle case where no documents are found
    if not documents:
        return {"response": "No relevant documents found.", "retrieved_docs": []}

    # Extracting text from s3 files and Preparing docs for LLM input
    s3_docs = [Document(page_content=get_s3_content_from_uri(doc[1]), metadata={"source": doc[0]}) for doc in documents]

    #s3_docs = [Document(page_content=text) for text in docs_text]

    # Load OpenAI model and generate answer
    # Using old model to save costs in querying
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    #creating a prompt for LLM to understand
    prompt = ChatPromptTemplate.from_template("""
    You are an accounting assistant that ONLY answers questions related to accounting based on the following context.
    If a query is not related to accounting, politely decline to answer even if the information exists in the context.
    Explain that you are specialized for accounting queries only and cannot assist with other topics.

    Accounting topics include: financial statements, bookkeeping, calculations, tax preparation, audit procedures, financial regulations, accounting principles (GAAP, IFRS), etc.
    Do not answer questions about non-accounting topics such as marketing, general business strategy, HR, or IT, even if this information appears in the context.

    Context: {context}

    Question: {question}

    Helpful answer:
    """)

    # Create a document chain that combines documents
    document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt, document_variable_name="context")


    # Run the chain with the s3 documents
    response = document_chain.invoke({
        "question": question,
        "context": s3_docs  # These are the documents you fetched from S3
    })

    return {"response": response, "retrieved_docs": [doc[0] for doc in documents]}