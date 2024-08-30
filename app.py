# # from fastapi import FastAPI, File, UploadFile, HTTPException
# # from fastapi.responses import JSONResponse
# # from pydantic import BaseModel
# # from typing import List
# # from langchain_community.llms import Ollama
# # from langchain_community.vectorstores import Chroma
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_community.embeddings.ollama import OllamaEmbeddings
# # from langchain_community.document_loaders import PDFPlumberLoader
# # from langchain.chains.combine_documents import create_stuff_documents_chain
# # from langchain.chains import create_retrieval_chain
# # from langchain.prompts import PromptTemplate
# # import os

# # app = FastAPI()

# # folder_path = "db"

# # cached_llm = Ollama(model="phi3:mini")

# # embedding = OllamaEmbeddings(model="mxbai-embed-large:latest")

# # text_splitter = RecursiveCharacterTextSplitter(
# #     chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
# # )

# # raw_prompt = PromptTemplate.from_template(
# #     """
# #     <s>[INST] You are a technical assistant good at searching documents. If you do not have an answer from the provided information say so. [/INST] </s>
# #     [INST] {input}
# #            Context: {context}
# #            Answer:
# #     [/INST]
# # """
# # )


# # class Query(BaseModel):
# #     query: str


# # class Source(BaseModel):
# #     source: str
# #     page_content: str


# # class ResponseAnswer(BaseModel):
# #     answer: str
# #     sources: List[Source] = []


# # @app.post("/ai", response_model=ResponseAnswer)
# # async def ai_post(query: Query):
# #     print("Post /ai called")
# #     print(f"query: {query.query}")

# #     response = cached_llm.invoke(query.query)

# #     print(response)

# #     return ResponseAnswer(answer=response)


# # @app.post("/ask_pdf", response_model=ResponseAnswer)
# # async def ask_pdf_post(query: Query):
# #     print("Post /ask_pdf called")
# #     print(f"query: {query.query}")

# #     print("Loading vector store")
# #     vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

# #     print("Creating chain")
# #     retriever = vector_store.as_retriever(
# #         search_type="similarity_score_threshold",
# #         search_kwargs={
# #             "k": 20,
# #             "score_threshold": 0.1,
# #         },
# #     )

# #     document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
# #     chain = create_retrieval_chain(retriever, document_chain)

# #     result = chain.invoke({"input": query.query})

# #     print(result)

# #     sources = [
# #         Source(source=doc.metadata["source"], page_content=doc.page_content)
# #         for doc in result["context"]
# #     ]

# #     return ResponseAnswer(answer=result["answer"], sources=sources)


# # # ... (keep all other imports as they were)

# # # ... (keep all other code before @app.post("/pdf") as it was)


# # @app.post("/pdf")
# # async def pdf_post(file: UploadFile = File(...)):
# #     if not file.filename.lower().endswith(".pdf"):
# #         raise HTTPException(status_code=400, detail="File must be a PDF")

# #     # Create the 'pdf' directory if it doesn't exist
# #     os.makedirs("pdf", exist_ok=True)

# #     save_file = f"pdf/{file.filename}"
# #     with open(save_file, "wb") as buffer:
# #         buffer.write(await file.read())

# #     print(f"filename: {file.filename}")

# #     loader = PDFPlumberLoader(save_file)
# #     docs = loader.load_and_split()
# #     print(f"docs len={len(docs)}")

# #     chunks = text_splitter.split_documents(docs)
# #     print(f"chunks len={len(chunks)}")

# #     vector_store = Chroma.from_documents(
# #         documents=chunks, embedding=embedding, persist_directory=folder_path
# #     )

# #     vector_store.persist()

# #     return JSONResponse(
# #         content={
# #             "status": "Successfully Uploaded",
# #             "filename": file.filename,
# #             "doc_len": len(docs),
# #             "chunks": len(chunks),
# #         }
# #     )


# # # ... (keep the rest of the code as it was)

# # if __name__ == "__main__":
# #     import uvicorn

# #     uvicorn.run(app, host="0.0.0.0", port=8080)
# import os
# import time
# from datetime import datetime
# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from typing import List
# from langchain_community.llms import Ollama
# from langchain_community.vectorstores import Chroma
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.embeddings.ollama import OllamaEmbeddings
# from langchain_community.document_loaders import PDFPlumberLoader
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
# from langchain.prompts import PromptTemplate

# app = FastAPI()

# folder_path = "db"

# cached_llm = Ollama(model="qwen2:0.5b")

# embedding = OllamaEmbeddings(model="mxbai-embed-large:latest")

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
# )

# raw_prompt = PromptTemplate.from_template(
#     """
#     <s>[INST] You are a technical assistant good at searching documents. If you do not have an answer from the provided information say so. [/INST] </s>
#     [INST] {input}
#            Context: {context}
#            Answer:
#     [/INST]
# """
# )


# class Query(BaseModel):
#     query: str


# class Source(BaseModel):
#     source: str
#     page_content: str


# class ResponseAnswer(BaseModel):
#     answer: str
#     sources: List[Source] = []


# def log_with_timestamp(message):
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
#     print(f"[{timestamp}] {message}")


# @app.post("/ai", response_model=ResponseAnswer)
# async def ai_post(query: Query):
#     log_with_timestamp("POST /ai called")
#     log_with_timestamp(f"Query: {query.query}")

#     start_time = time.perf_counter()
#     response = cached_llm.invoke(query.query)
#     end_time = time.perf_counter()

#     log_with_timestamp(f"LLM response time: {end_time - start_time:.4f} seconds")
#     log_with_timestamp(f"LLM response: {response}")

#     return ResponseAnswer(answer=response)


# @app.post("/ask_pdf", response_model=ResponseAnswer)
# async def ask_pdf_post(query: Query):
#     log_with_timestamp("POST /ask_pdf called")
#     log_with_timestamp(f"Query: {query.query}")

#     start_time = time.perf_counter()

#     log_with_timestamp("Loading vector store")
#     vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

#     log_with_timestamp("Creating chain")
#     retriever = vector_store.as_retriever(
#         search_type="similarity_score_threshold",
#         search_kwargs={
#             "k": 20,
#             "score_threshold": 0.1,
#         },
#     )

#     document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
#     chain = create_retrieval_chain(retriever, document_chain)

#     log_with_timestamp("Invoking chain")
#     result = chain.invoke({"input": query.query})

#     end_time = time.perf_counter()

#     log_with_timestamp(f"Total processing time: {end_time - start_time:.4f} seconds")
#     log_with_timestamp(f"Chain result: {result}")

#     sources = [
#         Source(source=doc.metadata["source"], page_content=doc.page_content)
#         for doc in result["context"]
#     ]

#     return ResponseAnswer(answer=result["answer"], sources=sources)


# @app.post("/pdf")
# async def pdf_post(file: UploadFile = File(...)):
#     start_time = time.perf_counter()
#     log_with_timestamp("POST /pdf called")

#     if not file.filename.lower().endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="File must be a PDF")

#     # Create the 'pdf' directory if it doesn't exist
#     os.makedirs("pdf", exist_ok=True)

#     save_file = f"pdf/{file.filename}"
#     with open(save_file, "wb") as buffer:
#         buffer.write(await file.read())

#     log_with_timestamp(f"File saved: {file.filename}")

#     loader = PDFPlumberLoader(save_file)
#     docs = loader.load_and_split()
#     log_with_timestamp(f"Document loaded and split, docs len={len(docs)}")

#     chunks = text_splitter.split_documents(docs)
#     log_with_timestamp(f"Text splitter applied, chunks len={len(chunks)}")

#     vector_store = Chroma.from_documents(
#         documents=chunks, embedding=embedding, persist_directory=folder_path
#     )

#     vector_store.persist()
#     log_with_timestamp("Vector store created and persisted")

#     end_time = time.perf_counter()
#     total_time = end_time - start_time
#     log_with_timestamp(f"Total processing time: {total_time:.4f} seconds")

#     return JSONResponse(
#         content={
#             "status": "Successfully Uploaded",
#             "filename": file.filename,
#             "doc_len": len(docs),
#             "chunks": len(chunks),
#             "processing_time": f"{total_time:.4f} seconds",
#         }
#     )


# # if __name__ == "__main__":
# #     import uvicorn

# #     uvicorn.run(app, host="0.0.0.0", port=8080)
import os
import time
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, AsyncGenerator
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate

app = FastAPI()

folder_path = "db"

cached_llm = Ollama(model="qwen2:0.5b")

embedding = OllamaEmbeddings(model="mxbai-embed-large:latest")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

raw_prompt = PromptTemplate.from_template(
    """ 
    <s>[INST] You are a technical assistant good at searching documents. If you do not have an answer from the provided information say so. [/INST] </s>
    [INST] {input}
        Context: {context}
        Answer:
    [/INST]
"""
)


class Query(BaseModel):
    query: str


class Source(BaseModel):
    source: str
    page_content: str


class ResponseAnswer(BaseModel):
    answer: str
    sources: List[Source] = []


def log_with_timestamp(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"[{timestamp}] {message}")


async def stream_response(generator: AsyncGenerator):
    """Utility to stream response line by line."""
    async for item in generator:
        yield item.encode("utf-8")


async def ai_response_generator(query: Query):
    """Async generator for streaming AI responses."""
    log_with_timestamp("POST /ai called")
    log_with_timestamp(f"Query: {query.query}")

    start_time = time.perf_counter()

    # Simulating streaming from LLM response
    for chunk in cached_llm.invoke(
        query.query, stream=True
    ):  # Assuming your LLM has a streaming option
        log_with_timestamp(f"Streamed chunk: {chunk}")
        yield chunk

    end_time = time.perf_counter()
    log_with_timestamp(f"Total LLM response time: {end_time - start_time:.4f} seconds")


@app.post("/ai", response_class=StreamingResponse)
async def ai_post(query: Query):
    return StreamingResponse(ai_response_generator(query), media_type="text/plain")


async def ask_pdf_response_generator(query: Query):
    """Async generator for streaming /ask_pdf responses."""
    log_with_timestamp("POST /ask_pdf called")
    log_with_timestamp(f"Query: {query.query}")

    start_time = time.perf_counter()

    log_with_timestamp("Loading vector store")
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

    log_with_timestamp("Creating chain")
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 20,
            "score_threshold": 0.1,
        },
    )

    document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
    chain = create_retrieval_chain(retriever, document_chain)

    log_with_timestamp("Invoking chain")
    for result in chain.invoke(
        {"input": query.query}, stream=True
    ):  # Assuming streaming is supported
        log_with_timestamp(f"Streamed result chunk: {result}")
        yield result

    end_time = time.perf_counter()
    log_with_timestamp(f"Total processing time: {end_time - start_time:.4f} seconds")


@app.post("/ask_pdf", response_class=StreamingResponse)
async def ask_pdf_post(query: Query):
    return StreamingResponse(ask_pdf_response_generator(query), media_type="text/plain")


async def pdf_post_response_generator(file: UploadFile):
    """Async generator for streaming PDF processing responses."""
    start_time = time.perf_counter()
    log_with_timestamp("POST /pdf called")

    if not file.filename.lower().endswith(".pdf"):
        yield "Error: File must be a PDF\n"
        log_with_timestamp("Error: File must be a PDF")
        return

    os.makedirs("pdf", exist_ok=True)

    save_file = f"pdf/{file.filename}"
    with open(save_file, "wb") as buffer:
        buffer.write(await file.read())

    log_with_timestamp(f"File saved: {file.filename}")

    loader = PDFPlumberLoader(save_file)
    docs = loader.load_and_split()
    log_with_timestamp(f"Document loaded and split, docs len={len(docs)}")

    chunks = text_splitter.split_documents(docs)
    log_with_timestamp(f"Text splitter applied, chunks len={len(chunks)}")

    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path
    )

    vector_store.persist()
    log_with_timestamp("Vector store created and persisted")

    end_time = time.perf_counter()
    total_time = end_time - start_time
    log_with_timestamp(f"Total processing time: {total_time:.4f} seconds")

    yield f"Successfully Uploaded {file.filename} | doc_len={len(docs)} | chunks={len(chunks)} | processing_time={total_time:.4f} seconds\n"


@app.post("/pdf")
async def pdf_post(file: UploadFile = File(...)):
    start_time = time.perf_counter()
    log_with_timestamp("POST /pdf called")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    # Create the 'pdf' directory if it doesn't exist
    os.makedirs("pdf", exist_ok=True)

    save_file = f"pdf/{file.filename}"
    with open(save_file, "wb") as buffer:
        buffer.write(await file.read())

    log_with_timestamp(f"File saved: {file.filename}")

    loader = PDFPlumberLoader(save_file)
    docs = loader.load_and_split()
    log_with_timestamp(f"Document loaded and split, docs len={len(docs)}")

    chunks = text_splitter.split_documents(docs)
    log_with_timestamp(f"Text splitter applied, chunks len={len(chunks)}")

    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path
    )

    vector_store.persist()
    log_with_timestamp("Vector store created and persisted")

    end_time = time.perf_counter()
    total_time = end_time - start_time
    log_with_timestamp(f"Total processing time: {total_time:.4f} seconds")

    return JSONResponse(
        content={
            "status": "Successfully Uploaded",
            "filename": file.filename,
            "doc_len": len(docs),
            "chunks": len(chunks),
            "processing_time": f"{total_time:.4f} seconds",
        }
    )


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(
#         app,
#         host="127.0.0.1",
#         port=8080,
#     )
