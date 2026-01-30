# Deploy RAG Chatbot with Document Upload as Portfolio Web App

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds.

This document must be maintained in accordance with PLANS.md at the repository root and with MULTI_AGENT_WORKFLOW_GUIDE.md for workflow and agent coordination.

## Purpose / Big Picture

After completing this plan, you will have a live, sustainable RAG chatbot web application hosted on Streamlit Community Cloud that you can use as a portfolio piece. Visitors can upload their own documents (PDFs and optionally plain text), have those documents chunked and indexed in-session, and then chat with a bot that uses only that uploaded context to answer questions. The app will also offer a “use default docs” mode so visitors can try it immediately with built-in Everstorm support docs. For this plan, "use default docs" means **fallback when no upload exists**: if the user has not uploaded and indexed documents in this session, the app uses the default Everstorm index. No separate "Use default docs" toggle or button is required unless the plan is later updated. The app will be accessible via a public URL, will update on git push, and will support both local runs (with Ollama) and cloud runs (with a configurable API-backed LLM when Ollama is unavailable).

To see it working, you will open the deployed Streamlit app URL, optionally upload one or more PDFs, click to index them, then ask questions in the chat; answers will be grounded in the uploaded (or default) documents. You will observe a clear title, an upload/index area, a chat history, and a chat input.

**This plan uses an automated multi-agent workflow.** Three agents work in sequence using Git work trees: one develops the app and upload-and-index feature, one reviews code quality, and one verifies plan alignment and merges. The workflow runs against a separate GitHub repository you create for this deployment, keeping the course project untouched.

### How this document is organized

Different sections serve different roles; they are complementary, not redundant:

- **Plan of Work (Parts 1–4):** *What* to build — the **scope** (Streamlit UI, upload/index, default docs + LLM, deployment artifacts). “Parts” = deliverables.
- **Concrete Steps:** *How* to build it — the **implementation procedure** (Steps 1.1–1.6 for Agent 1, 2.x for Agent 2, 3.x for Agent 3). “Steps” = actions.
- **Workflow Orchestration and Agent Coordination:** *How* agents work together — **sequence, checkpoints, handoffs**, iteration, and recovery. Who does what *when*, and how they signal readiness.
- **Progress:** A **tracking checklist** in execution order. It mirrors the workflow sequence and aligns with Concrete Steps; use it to check off work as you go.

**Review model:** Agent 1 implements *all* of the plan (Parts 1–4, i.e. Steps 1.1–1.6), then opens **one** pull request. Agent 2 reviews that PR, then Agent 3 verifies plan alignment and merges. Review and alignment happen **once per PR**, not after each development step. If changes are requested, Agent 1 updates the PR and the cycle repeats until the PR is merged.

## Progress

This checklist follows the **Workflow Orchestration** sequence. Check off items as you complete them.

**Initial trigger (Human — one time)**

- [ ] Create separate GitHub repository for the RAG deployment project
- [ ] Initialize repository with this ExecPlan and source references (notebook and project_2)
- [ ] Ensure agents have repo URL, source paths, and main branch name

**Agent 1 (Development) — implement then open one PR**

- [ ] Set up git work tree and feature branch (Step 1.1)
- [ ] Implement core app and Step 6 UI (Step 1.2)
- [ ] Add document upload, chunking, and in-session FAISS indexing (Step 1.3)
- [ ] Add default index and configurable LLM (Step 1.4)
- [ ] Add requirements.txt and README (Step 1.5)
- [ ] Commit, push, and open PR (Step 1.6) → **Checkpoint: PR ready for review**

**Agent 2 (Code Review)**

- [ ] Review PR for structure, error handling, safety (Steps 2.1–2.2) → **Checkpoint: approved or change requests**

**Agent 3 (Plan Alignment)**

- [ ] Verify implementation matches ExecPlan; resolve conflicts if any; merge when satisfied (Steps 3.1–3.2) → **Checkpoint: merged or fixes requested**

**Iteration (if needed)**

- [ ] Agent 1 addresses feedback, updates PR; Agent 2 and Agent 3 repeat until PR is merged

**Completion**

- [ ] Main branch has deployable app; work tree removed; repo ready for Streamlit Cloud
- [ ] Final verification: test deployment readiness and document live URL (Human)

## Surprises & Discoveries

(To be populated during implementation)

## Decision Log

- Decision: Base implementation on notebook Step 6 and existing project_2 app.py where useful  
  Rationale: Step 6 defines the minimal Streamlit chat loop and chain invocation; app.py already has FAISS loading, retriever, and chain construction. Reuse patterns and extend rather than rewrite from scratch.  
  Date/Author: (fill when executing)

- Decision: Support document upload and in-session indexing as the main portfolio differentiator  
  Rationale: User requested that people can upload documents, have them indexed, and have the RAG use those documents as context. That is the core added behavior beyond “run Step 6.”  
  Date/Author: (fill when executing)

- Decision: Keep uploaded-document index session-scoped (in-memory FAISS, no persistence on Streamlit Cloud)  
  Rationale: Streamlit Community Cloud has an ephemeral filesystem; there is no durable disk for user uploads. In-session indexing is sustainable, free, and requires no external vector DB or secrets. Persistence across sessions would require an external store and is out of scope for this plan.  
  Date/Author: (fill when executing)

- Decision: Make LLM backend configurable so the app works locally (Ollama) and on Streamlit Cloud (e.g. OpenAI/Groq via API key in secrets)  
  Rationale: Ollama does not run on Streamlit Community Cloud. For a permanently hosted portfolio app, the cloud instance must use an API-backed LLM. Configurable backend keeps one codebase for local demos and cloud deployment.  
  Date/Author: (fill when executing)

- Decision: Deploy to Streamlit Community Cloud from a dedicated GitHub repository  
  Rationale: Free, permanent public URL, auto-deploy on push, and clean separation from the course repo so the portfolio piece is self-contained and shareable.  
  Date/Author: (fill when executing)

- Decision: Use the multi-agent workflow (Development, Code Review, Plan Alignment) with git work trees  
  Rationale: Aligns with MULTI_AGENT_WORKFLOW_GUIDE.md; reduces manual steps, enforces quality and plan adherence, and provides clear checkpoints for recovery.  
  Date/Author: (fill when executing)

## Outcomes & Retrospective

(To be populated upon completion)

## Context and Orientation

The RAG chatbot lives in the `project_2` directory of this repository. The main artifacts are:

- **project_2/rag_chatbot.ipynb** — Jupyter notebook that builds the RAG pipeline in six steps. Step 6 (“Build the Streamlit UI”) defines a minimal `app.py`-style script: Streamlit title, chat history in session state, chat input, and invocation of a `chain` with `question` and `chat_history`. The chain and retriever are built in earlier steps from FAISS, embeddings, and an Ollama LLM.
- **project_2/app.py** — Existing Streamlit app that loads a pre-built FAISS index from `faiss_index/`, builds a ConversationalRetrievalChain with a filtered retriever, and runs the chat loop. It does not support document upload or in-session indexing.
- **project_2/environment.yml** — Conda environment (Python 3.11) with LangChain, LangChain Community, sentence-transformers, Streamlit, FAISS, unstructured, etc. Deployment will use an equivalent `requirements.txt`.

Relevant notebook concepts used in this plan:

- **Chunking**: `RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)` splits documents into overlapping chunks for embedding.
- **Embeddings**: `SentenceTransformerEmbeddings(model_name="thenlper/gte-small")` (or configurable) produces vectors for chunks and queries.
- **Vector store**: FAISS holds chunk embeddings; `FAISS.from_documents(chunks, embeddings)` builds an index; `vectordb.as_retriever(search_kwargs={"k": 8})` exposes retrieval.
- **RAG chain**: `ConversationalRetrievalChain.from_llm(llm, retriever, combine_docs_chain_kwargs={"prompt": prompt})` with a system prompt that restricts answers to provided context.

**Document upload and indexing (new):** Users upload PDF (and optionally .txt) files via Streamlit’s `st.file_uploader`. The app chunks each document with the same splitter, embeds chunks with the same embedding model, and builds a FAISS index in memory for that session. The RAG chain uses this session index as the retriever. If no documents are uploaded, the app can load a default corpus (e.g. pre-bundled Everstorm PDFs or a pre-built index in the repo) so visitors see immediate value.

**Streamlit Community Cloud:** Hosting is ephemeral; app runs in the cloud, filesystem does not persist between deploys or sessions. User-uploaded data exists only for the duration of the session. The LLM cannot be Ollama on Cloud; use environment variables or Streamlit secrets to switch to an API-based LLM (e.g. OpenAI, Groq).

**Multi-Agent Workflow:** Follow MULTI_AGENT_WORKFLOW_GUIDE.md. Agent 1 develops in a git work tree and opens a PR; Agent 2 reviews code; Agent 3 checks alignment with this ExecPlan, resolves conflicts, and merges. All coordination is via Git and GitHub (PRs, comments, merge).

## Workflow Orchestration and Agent Coordination

This section describes *how* agents coordinate: sequence, checkpoints, handoffs, and recovery. The **Progress** checklist above mirrors this sequence for tracking. The detailed *what* to build is in **Plan of Work (Parts 1–4)**; the detailed *how* to implement it is in **Concrete Steps** below.

**Initial Trigger (Human Action — One Time):**

1. Create a new GitHub repository for this deployment (e.g. `rag-chatbot-portfolio`).
2. Push this ExecPlan to the repository (e.g. as `RAG_PORTFOLIO_DEPLOYMENT_PLAN.md` or equivalent).
3. Provide agents with:
   - Repository URL (e.g. `https://github.com/yourusername/rag-chatbot-portfolio`)
   - Source paths: `project_2/rag_chatbot.ipynb`, `project_2/app.py`, `project_2/environment.yml`, and `project_2/data/` (or a zip/export of default docs)
   - Main branch name (e.g. `main`)

**Agent Execution Sequence:**

1. **Agent 1 (Development)**  
   - Follow **Concrete Steps 1.1–1.6** (work tree, UI, upload/index, default index + LLM, requirements + README, commit + PR). Implements *all* of Parts 1–4, then opens **one** pull request targeting main.  
   - **Checkpoint:** PR created and ready for review.

2. **Agent 2 (Code Review)**  
   - Follow **Concrete Steps 2.1–2.2**: review PR for structure, error handling, safety; approve or request changes via PR comments.  
   - **Checkpoint:** PR approved or change requests documented.

3. **Agent 3 (Plan Alignment)**  
   - If Agent 2 requested changes, waits for Agent 1 to update the PR.  
   - Follow **Concrete Steps 3.1–3.2**: verify implementation matches ExecPlan, resolve conflicts if any, merge when satisfied.  
   - **Checkpoint:** PR merged to main or specific fixes requested from Agent 1.

4. **Iteration:** If Agent 2 or Agent 3 request fixes, Agent 1 pushes new commits; review and alignment repeat until the PR is merged.

5. **Completion:** Main branch contains the deployable app; work tree is removed; repo is ready to connect to Streamlit Community Cloud.

**Agent Communication:** Handoffs are via PR state and comments. Agent 1 signals readiness by opening/updating the PR; Agent 2 and Agent 3 signal outcomes via review and merge.

**Work Tree Management:** Agent 1 uses a temporary work tree (e.g. `/tmp/rag-chatbot-dev-worktree`) and a dedicated feature branch. Agent 2 and Agent 3 operate on the same repo (e.g. via clone or existing checkout); only Agent 1 needs a separate work tree for implementation.

**Recovery:** If any agent fails, work remains in Git. Resume from the last checkpoint: re-run the same agent or continue with the next one after Agent 1 addresses feedback.

## Plan of Work

*What* to build — the scope. Implementation procedure is in **Concrete Steps**; coordination is in **Workflow Orchestration**; tracking is in **Progress**.

The work has four main parts: implementing the Step 6 Streamlit UI, adding document upload and in-session indexing, making the LLM configurable for local vs cloud, and preparing deployment.

**Part 1 — Streamlit UI from Step 6**

Implement the minimal chat UI implied by notebook Step 6: `st.title`, session state for `messages` and `chat_history`, display of past messages with `st.chat_message`, `st.chat_input`, and on each user message invoke the RAG chain with `question` and `chat_history`, then append the assistant reply to both `messages` and `chat_history`. Reuse the system prompt and chain structure from the notebook (and from app.py where it already matches). Ensure the entry point runs `streamlit run app.py`.

**Part 2 — Document upload and in-session indexing**

Add a section (e.g. sidebar or top section) where users can upload files. Accept at least PDF; optionally TXT. Use the same loaders as in the notebook (e.g. `PyPDFLoader` for PDF, `TextLoader` for TXT). For each uploaded file, load documents into a list, then chunk with `RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)`. Use the same embedding model as the rest of the app (e.g. `thenlper/gte-small`). Build a FAISS index with `FAISS.from_documents(chunks, embeddings)` and store it in session state (e.g. `st.session_state["vectordb"]` and `st.session_state["retriever"]`). Provide a clear “Index documents” or “Use these documents” action so the user triggers indexing after upload. When building the RAG chain, use the session retriever if it exists; otherwise fall back to a default (see Part 3). After indexing, optionally clear or replace chat history so the next answers use the new context. **Chain lifecycle:** `ConversationalRetrievalChain` takes the retriever at construction. When switching between default and uploaded index, rebuild the chain with the current retriever; do not reuse a cached chain built for the other retriever. **FilteredRetriever:** Apply filtering (e.g. exclude BigCommerce API docs) only to the default Everstorm index. For user-uploaded documents, use a plain retriever (no filtering).

**Document upload — explicit steps (implementation check-list):**

1. **UI:** Add `st.file_uploader` for PDF (and optionally `.txt`) in sidebar or a dedicated section. Restrict accepted types (e.g. `type=["pdf","txt"]`); validate file types before processing and reject non-PDF / non-TXT.
2. **Action:** Add an "Index documents" (or "Use these documents") **button**. Enable it only when at least one file is selected; disable or hide when no files are selected.
3. **On Index click:** (a) Load each file with `PyPDFLoader` (PDF) or `TextLoader` (TXT), append to `all_docs`. (b) Chunk with `RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30).split_documents(all_docs)`. (c) Embed and build `FAISS.from_documents(chunks, embeddings)`. (d) Store in `st.session_state["vectordb"]` and `st.session_state["retriever"]`. (e) Optionally clear `messages` and `chat_history` so the next answers use the new context. (f) On load, chunk, or index failure (e.g. corrupt PDF, empty file), show a user-visible error (e.g. `st.error`) and **do not** overwrite the session index.
4. **Empty uploads:** If Index is clicked with no files selected (or all removed), show a brief message (e.g. `st.warning`) and do nothing; do not clear any existing session index.
5. **Switching:** Use session retriever when present, else default index. Rebuild the chain when the active retriever changes (default ↔ uploaded).
6. **Optional — TXT support:** If supporting `.txt`, add it as an accepted type and use `TextLoader` for those files; document in README.

**Part 3 — Default docs and configurable LLM**

If no upload has been done in this session, the app should still work. Either (a) ship a small default corpus (e.g. under `data/` or `default_docs/`) and build a FAISS index from it at startup (or on first load), or (b) ship a pre-built FAISS index in the repo and load it when no session index exists. The plan prefers (b) for Cloud so no heavy CPU at startup; (a) is acceptable if indexing is fast and one-time. Document which default docs or index are used.

Make the LLM backend configurable. If running where Ollama is available (e.g. local), use `Ollama(model=..., temperature=...)`. If not (e.g. on Streamlit Cloud), use an API-based LLM driven by environment variables or Streamlit secrets (e.g. `OPENAI_API_KEY` and use an OpenAI-chat or compatible client). The plan does not mandate a specific cloud LLM; specify one option (e.g. OpenAI) in the ExecPlan and in README so the deployer knows what to set. Local runs can rely on `ollama` being installed and `ollama serve` + model pull.

**Part 4 — Deployment artifacts**

Add a `requirements.txt` that mirrors the notebook/app stack: streamlit, langchain, langchain-community, sentence-transformers, faiss-cpu, unstructured (and pypdf if not pulled in by unstructured), plus any LLM client (e.g. openai) for Cloud. Add a README that explains: (1) local setup (clone, `pip install -r requirements.txt`, optional Ollama setup, `streamlit run app.py`), (2) deployment on Streamlit Community Cloud (connect repo, set main file to `app.py`, configure secrets/env for API key if using API-backed LLM), (3) that uploaded documents are session-scoped and that default docs/index provide a ready-to-use demo.

Implementation can live in a single `app.py` or be split into modules (e.g. `rag.py` for chain/retriever building, `app.py` for Streamlit). The ExecPlan assumes one deployable entrypoint `app.py` that Streamlit Cloud can run.

## Concrete Steps

*How* to implement — the detailed procedure. Scope is in **Plan of Work (Parts 1–4)**; coordination is in **Workflow Orchestration**; tracking is in **Progress**.

**Prerequisites (Human — One Time)**

1. Create GitHub repo (e.g. `rag-chatbot-portfolio`).  
2. Push this ExecPlan and, if desired, a reference to the source (e.g. copy of plan + note that sources are in `project_2/` of the course repo).  
3. Ensure agents can read the notebook and project_2 files (either by committing them into the new repo or by giving agents access to the course repo path).

**Agent 1 — Development**

**Step 1.1 — Work tree and branch**

    REPO_URL="<deployment-repo-url>"
    WORK_TREE_DIR="/tmp/rag-chatbot-dev-worktree"
    REPO_DIR="/tmp/rag-chatbot-repo"
    git clone $REPO_URL $REPO_DIR && cd $REPO_DIR
    git worktree add $WORK_TREE_DIR -b feature/streamlit-rag-upload
    cd $WORK_TREE_DIR

**Step 1.2 — Implement core app and Step 6 UI**

In the work tree root, create or update `app.py` so it:

- Imports streamlit, LangChain components (FAISS, embeddings, chain, prompt), and any loaders (PyPDFLoader, TextLoader).
- Defines the same system prompt as in the notebook (answer only from context; say “I don’t know based on the documents” when absent).
- Initializes `st.session_state` for `messages`, `chat_history`, and (for later steps) `vectordb` / `retriever` and `chain`.
- Renders title and chat history, then `st.chat_input`. On user input, invokes the RAG chain with `question` and `chat_history` and updates session state. Use a placeholder or default retriever/chain until Step 1.3 and 1.4 are done so the app runs without errors.

**Step 1.3 — Document upload and in-session indexing**

- Add `st.file_uploader` for PDF (and optionally TXT), e.g. in sidebar or above chat. Restrict accepted types (e.g. `type=["pdf","txt"]`); validate file types before processing and reject non-PDF / non-TXT.
- Add an “Index documents” (or “Use these documents”) **button**; enable it only when at least one file is selected. If Index is clicked with no files, show a brief message (e.g. `st.warning`) and do nothing.
- On “Index” click: for each uploaded file, load pages/documents (PyPDFLoader/TextLoader), append to a docs list, run `RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30).split_documents(all_docs)`.
- Build embeddings with the same model used elsewhere (e.g. `SentenceTransformerEmbeddings(model_name="thenlper/gte-small")`), then `FAISS.from_documents(chunks, embeddings)`.
- Save in session: `st.session_state["vectordb"] = vectordb`, `st.session_state["retriever"] = vectordb.as_retriever(search_kwargs={"k": 8})`. Use a **plain** retriever for uploaded docs (no FilteredRetriever).
- When building the chain, use `st.session_state["retriever"]` if present; otherwise use the default index (Step 1.4). **Rebuild the chain** when the active retriever changes (default ↔ uploaded); do not reuse a cached chain for the other retriever.
- Use `@st.cache_resource` only for embedding model and other stateless objects; keep per-session index in session state.
- **Error handling:** On load, chunk, or index failure (e.g. corrupt PDF, empty file), show a user-visible error (e.g. `st.error`) and **do not** overwrite the session index.
- **Optional:** After indexing, clear or replace `messages` and `chat_history` so the next answers use the new context (see Part 2).

**Step 1.4 — Default index and configurable LLM**

- Default index: either include a pre-built `faiss_index/` in the repo and load it when `st.session_state.get("retriever")` is None, or load default PDFs from `data/` (or `default_docs/`), chunk and index once (e.g. cached or at startup), and use that retriever when no upload exists. Apply **FilteredRetriever** only to the default index (e.g. exclude BigCommerce API docs); uploaded docs use a plain retriever (Step 1.3). Specify in code and README which strategy is used.
- LLM: if `OLLAMA_BASE_URL` or a similar “use Ollama” signal is set and reachable, use `Ollama(model="gemma3:1b", temperature=0.1)`. Otherwise use an API-based LLM (e.g. OpenAI) with API key from `os.environ.get("OPENAI_API_KEY")` or `st.secrets`. Document in README that Cloud deployers must set the API key (or equivalent) for the cloud backend.

**Step 1.5 — requirements.txt and README**

- `requirements.txt`: streamlit, langchain, langchain-community, sentence-transformers, faiss-cpu, unstructured, pypdf; add openai (or chosen API client) if using OpenAI on Cloud.
- README: purpose of the app; local run steps; Streamlit Community Cloud deploy steps; note on session-scoped uploads and default docs; required env/secrets for Cloud LLM.

**Step 1.6 — Commit and open PR**

    cd $WORK_TREE_DIR
    git add app.py requirements.txt README.md
    git add faiss_index/   # if shipping pre-built default index
    git commit -m "feat: RAG chatbot with document upload and Streamlit Cloud deployment"
    git push origin feature/streamlit-rag-upload
    gh pr create --base main --title "RAG chatbot with upload and deployment" --body "Implements ExecPlan: Step 6 UI, upload+index, configurable LLM, deployment ready."

**Agent 2 — Code Review**

- Step 2.1: Review PR for structure, error handling (missing files, empty uploads, index build failures), and safety (no arbitrary code execution from uploads; validate file types).
- Step 2.2: Approve or request changes via PR comments.

**Agent 3 — Plan Alignment**

- Step 3.1: Confirm presence of upload UI, indexing path, default-docs path, configurable LLM, `requirements.txt`, README.
- Step 3.2: Resolve merge conflicts if any; merge when satisfied.

**Final step — Deploy on Streamlit Community Cloud (Human)**

- In share.streamlit.io: New app → connect repo → branch main → main file `app.py`. Add secrets or env vars for the Cloud LLM API key if used. Deploy and note the public URL.

## Validation and Acceptance

- **Local run:** From the work tree (or main after merge), `streamlit run app.py` starts the app. With default docs/index, a visitor can ask a question and get an answer grounded in context. With uploads, after uploading at least one PDF and triggering “Index,” answers use the uploaded content (e.g. ask “What does this document say about X?” and receive an answer referencing the upload).
- **Upload and index:** Uploading PDFs and clicking the index action creates a session retriever; the next questions use that retriever. No persistence after refresh.
- **Configurable LLM:** With Ollama running and default env, answers are generated locally. With Ollama off and `OPENAI_API_KEY` set (and code path for OpenAI enabled), answers are generated via the API.
- **Deployment:** After connecting the repo to Streamlit Community Cloud and setting the API key (if used), the app builds and runs; the public URL shows the same UI and supports default docs and upload-and-index in session.

## Idempotence and Recovery

- Cloning, work-tree creation, and branch creation are idempotent in the sense that repeating them with the same branch name may require deleting an existing work tree or branch first; document “cleanup” as in MULTI_AGENT_WORKFLOW_GUIDE (e.g. `git worktree remove …`, `git branch -d …`).
- All app logic is additive: uploads do not overwrite repo contents; session state is per-run. Re-running the app or re-indexing in the same session is safe.
- If the PR is closed or the branch deleted, Agent 1 can recreate the branch and PR from the same local work tree or a fresh one; no unique state is lost beyond unmerged commits.

## Artifacts and Notes

Expected layout of the deployment repository after implementation:

    rag-chatbot-portfolio/
      app.py              # Streamlit app: upload UI, indexing, chat, configurable LLM
      requirements.txt    # Dependencies for local and Cloud
      README.md          # Setup and deployment instructions
      faiss_index/       # (optional) Pre-built default index
      data/ or default_docs/  # (optional) Default PDFs if not using pre-built index
      RAG_PORTFOLIO_DEPLOYMENT_PLAN.md  # This ExecPlan

The course `project_2/` directory remains unchanged; this plan produces a separate, deployable project.

## Interfaces and Dependencies

- **Streamlit:** `st.title`, `st.chat_message`, `st.chat_input`, `st.file_uploader`, `st.session_state`, `st.spinner`, `st.cache_resource` (for embedding model only where appropriate; see below).
- **LangChain:** `RecursiveCharacterTextSplitter`, `PyPDFLoader`, `TextLoader` (or equivalents from langchain_community), `FAISS.from_documents` / `FAISS.load_local`, `SentenceTransformerEmbeddings`, `ConversationalRetrievalChain.from_llm`, `PromptTemplate`. Retriever from `vectordb.as_retriever(search_kwargs={"k": 8})`. Use **k=8** for retrieval in the deployable app (default and uploaded index).
- **LLM:** `Ollama(model="gemma3:1b", temperature=0.1)` when local; when Cloud, a callable or LangChain LLM instance backed by OpenAI (or documented alternative) using `OPENAI_API_KEY` or Streamlit secrets.
- **Chunking:** `RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)`.
- **Embeddings:** `SentenceTransformerEmbeddings(model_name="thenlper/gte-small")` unless overridden by env.

**Implementation notes:** Cache only the embedding model (and optionally the LLM) with `@st.cache_resource`; keep the per-session index in session state. Build the RAG chain per retriever when it is used (default vs uploaded); do not cache the chain, since it must be rebuilt when switching retrievers.

System prompt must include placeholders `{context}` and `{question}` and instruct the model to answer only from the provided context and to refuse when the answer is not in the context.
