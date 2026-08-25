# Chatbot Builder Backend API

A FastAPI backend designed for building custom chatbots. It supports user authentication, document uploading (PDFs, DOCX, CSVs, JSON, Markdown, and web pages), text chunking, embedding generation using Cohere, and background processing via Celery and Redis.

## Technical Stack
* **Framework**: FastAPI (Python)
* **Database**: PostgreSQL (pgvector for vector embeddings)
* **Migrations**: Alembic
* **Background Workers**: Celery + Redis
* **Ingestion/Parsing**: LangChain, PyPDF, python-docx, BeautifulSoup4
* **Vector Store**: pgvector + SQLAlchemy
* **Embeddings Provider**: Cohere API

---

## Folder Structure

Below is the directory layout of the workspace. Click any of the files or folders to navigate to them:

```text
backend/
├── alembic.ini                             # [alembic.ini](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/alembic.ini) - Alembic configuration file
├── requirements.txt                         # [requirements.txt](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/requirements.txt) - Backend package dependencies
├── alembic/                                 # Database migrations folder
│   ├── env.py                               # [alembic/env.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/alembic/env.py) - Migration environment setup
│   ├── script.py.mako                       # [alembic/script.py.mako](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/alembic/script.py.mako) - Migration script template
│   └── versions/                            # Migration scripts
│       ├── 6dd705678c4b_embeddings_in_document_chunk.py
│       └── 77c2a33e4e10_embedding_size_to_1536.py
├── app/                                     # Core application package
│   ├── __init__.py                          # [app/__init__.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/__init__.py)
│   ├── main.py                              # [app/main.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/main.py) - App entrypoint & routers setup
│   ├── core/                                # Core configurations & client initializers
│   │   ├── celery.py                        # [app/core/celery.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/core/celery.py) - Celery instance and settings
│   │   ├── config.py                        # [app/core/config.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/core/config.py) - Environment config loader
│   │   ├── security.py                      # [app/core/security.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/core/security.py) - Password hashing & JWT helpers
│   │   └── supabase.py                      # [app/core/supabase.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/core/supabase.py) - Supabase integration
│   ├── database/                            # Database setup
│   │   ├── base.py                          # [app/database/base.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/database/base.py) - Imports all models for Alembic auto-generation
│   │   └── db.py                            # [app/database/db.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/database/db.py) - Engine, SessionLocal, and DB Base model definition
│   ├── dependencies/                        # FastAPI dependency injections
│   │   └── auth.py                          # [app/dependencies/auth.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/dependencies/auth.py) - Current user session checker
│   ├── embeddings/                          # Embedding services & providers
│   │   ├── embedding_service.py             # [app/embeddings/embedding_service.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/embeddings/embedding_service.py) - Interface for embedding generators
│   │   ├── provider_factory.py              # [app/embeddings/provider_factory.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/embeddings/provider_factory.py) - Resolves providers dynamically
│   │   └── providers/
│   │       ├── base.py                      # [app/embeddings/providers/base.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/embeddings/providers/base.py) - Base provider interface
│   │       └── cohere_provider.py            # [app/embeddings/providers/cohere_provider.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/embeddings/providers/cohere_provider.py) - Cohere Client embedding implementation
│   ├── ingestion/                           # Document ingestion logic
│   │   ├── ingestion_service.py             # [app/ingestion/ingestion_service.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/ingestion/ingestion_service.py) - Main service coordination for parsing
│   │   ├── loader_factory.py                # [app/ingestion/loader_factory.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/ingestion/loader_factory.py) - Factory to return loader by file extension
│   │   ├── splitter.py                      # [app/ingestion/splitter.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/ingestion/splitter.py) - Splits documents into chunks
│   │   └── loaders/                         # Type-specific loaders
│   │       ├── base.py                      # [app/ingestion/loaders/base.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/ingestion/loaders/base.py) - Base Loader interface
│   │       ├── csv_loader.py                # [app/ingestion/loaders/csv_loader.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/ingestion/loaders/csv_loader.py)
│   │       ├── docx_loader.py               # [app/ingestion/loaders/docx_loader.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/ingestion/loaders/docx_loader.py)
│   │       ├── json_loader.py               # [app/ingestion/loaders/json_loader.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/ingestion/loaders/json_loader.py)
│   │       ├── markdown_loader.py           # [app/ingestion/loaders/markdown_loader.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/ingestion/loaders/markdown_loader.py)
│   │       ├── pdf_loader.py                # [app/ingestion/loaders/pdf_loader.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/ingestion/loaders/pdf_loader.py)
│   │       ├── text_loader.py               # [app/ingestion/loaders/text_loader.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/ingestion/loaders/text_loader.py)
│   │       └── web_loader.py                # [app/ingestion/loaders/web_loader.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/ingestion/loaders/web_loader.py)
│   ├── models/                              # SQLAlchemy Models
│   │   ├── chatbot.py                       # [app/models/chatbot.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/models/chatbot.py) - Chatbot definition
│   │   ├── document.py                      # [app/models/document.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/models/document.py) - Document definition
│   │   ├── document_chunk.py                # [app/models/document_chunk.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/models/document_chunk.py) - DocumentChunk definition (stores Vector embedding)
│   │   └── user.py                          # [app/models/user.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/models/user.py) - User definition
│   ├── routers/                             # FastAPI API Route Controllers
│   │   ├── auth.py                          # [app/routers/auth.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/routers/auth.py) - User sign-up/login routes
│   │   ├── chatbots.py                      # [app/routers/chatbots.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/routers/chatbots.py) - CRUD endpoints for bots
│   │   └── documents.py                     # [app/routers/documents.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/routers/documents.py) - Document upload and retrieval routes
│   ├── schemas/                             # Pydantic Schemas (Request/Response validators)
│   │   ├── auth.py                          # [app/schemas/auth.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/schemas/auth.py)
│   │   ├── chatbot.py                       # [app/schemas/chatbot.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/schemas/chatbot.py)
│   │   ├── document.py                      # [app/schemas/document.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/schemas/document.py)
│   │   └── user.py                          # [app/schemas/user.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/schemas/user.py)
│   ├── services/                            # Business Logic Layer
│   │   ├── auth_service.py                  # [app/services/auth_service.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/services/auth_service.py) - Authentication routines
│   │   ├── chatbot_service.py               # [app/services/chatbot_service.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/services/chatbot_service.py) - ChatbotService CRUD helpers
│   │   ├── document_embedding_service.py    # [app/services/document_embedding_service.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/services/document_embedding_service.py) - Coordinate splits and embeddings
│   │   ├── document_service.py              # [app/services/document_service.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/services/document_service.py) - File upload & record persistence
│   │   └── vector_service.py                # [app/services/vector_service.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/services/vector_service.py) - Embedding storage & querying
│   ├── storage/                             # Uploaded file persistence providers
│   │   ├── base.py                          # [app/storage/base.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/storage/base.py) - Storage handler interface
│   │   ├── local_storage.py                 # [app/storage/local_storage.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/storage/local_storage.py) - File system saving
│   │   └── supabase_storage.py              # [app/storage/supabase_storage.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/storage/supabase_storage.py) - Cloud bucket integration
│   ├── tasks/                               # Celery Tasks
│   │   └── document_tasks.py                # [app/tasks/document_tasks.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/tasks/document_tasks.py) - Asynchronous document processing task definitions
│   └── vectorstore/                         # Vector Querying & Search
│       ├── retriever.py                     # [app/vectorstore/retriever.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/vectorstore/retriever.py) - Chunk retrieval strategies
│       └── vector_store_service.py          # [app/vectorstore/vector_store_service.py](file:///c:/Users/hp/Desktop/portfolio/personal%20projects/agentbuilder/backend/app/vectorstore/vector_store_service.py) - Vector database actions
```
