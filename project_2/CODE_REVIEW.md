# Code Review: app.py

**Date:** 2026-01-25  
**Reviewer:** AI Code Review  
**File:** `project_2/app.py`

---

## Executive Summary

The code is functional and well-structured, but there are several areas for improvement including deprecated imports, error handling, type hints, and code organization. Overall rating: **7/10**

---

## 🔴 Critical Issues

### 1. **Deprecated LangChain Imports** (Lines 2-6)
**Severity:** High  
**Impact:** Code will break in future LangChain versions

**Current:**
```python
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.llms import Ollama
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
```

**Recommended:**
```python
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import ConversationalRetrievalChain  # Still valid
from langchain.prompts import PromptTemplate  # Still valid
```

**Action:** Update imports to use `langchain_community` package.

---

## 🟡 Major Issues

### 2. **Missing Type Hints** (Multiple locations)
**Severity:** Medium  
**Impact:** Reduced code maintainability and IDE support

**Issues:**
- `filter_documents()` function lacks return type hint
- Function parameters lack type hints
- Missing type hints reduce code clarity

**Recommended:**
```python
def filter_documents(
    docs: List[Document], 
    exclude_keywords: List[str] | None = None
) -> List[Document]:
    """Filter out documents from excluded sources."""
    ...
```

### 3. **Inefficient Document Filtering Logic** (Lines 38-39)
**Severity:** Medium  
**Impact:** Redundant string operations

**Current:**
```python
if "data/everstorm" in source or ("everstorm" in source.lower() and ".pdf" in source):
```

**Issue:** `source` is already lowercased on line 36, so `source.lower()` is redundant.

**Recommended:**
```python
if "data/everstorm" in source or ("everstorm" in source and ".pdf" in source):
```

### 4. **Duplicate Code for Filename Extraction** (Lines 139-144, 158-162)
**Severity:** Medium  
**Impact:** Code duplication, maintenance burden

**Issue:** Same logic repeated twice for extracting filename from path.

**Recommended:** Extract to a helper function:
```python
def extract_filename(source: str) -> str:
    """Extract filename from a file path."""
    return source.split('/')[-1] if '/' in source else source
```

### 5. **Error Handling Could Be More Specific** (Line 168)
**Severity:** Medium  
**Impact:** Generic error messages don't help debugging

**Current:**
```python
except Exception as e:
    response = f"Sorry, I encountered an error: {str(e)}. Please try again or rephrase your question."
    st.error(f"Error: {str(e)}")
```

**Recommended:** Handle specific exceptions:
```python
except FileNotFoundError as e:
    response = "The vector database could not be found. Please ensure the FAISS index is built."
    st.error(f"File not found: {str(e)}")
except ConnectionError as e:
    response = "Could not connect to the LLM service. Please ensure Ollama is running."
    st.error(f"Connection error: {str(e)}")
except Exception as e:
    response = "Sorry, I encountered an unexpected error. Please try again."
    st.error(f"Error: {str(e)}")
    st.exception(e)  # Show full traceback in debug mode
```

### 6. **Hardcoded Configuration Values** (Lines 73, 76, 79, 88)
**Severity:** Medium  
**Impact:** Difficult to configure without code changes

**Issues:**
- Embedding model name hardcoded
- FAISS index path hardcoded
- Retrieval `k` value hardcoded
- LLM model and temperature hardcoded

**Recommended:** Use environment variables or Streamlit config:
```python
import os

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "thenlper/gte-small")
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index")
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "12"))
LLM_MODEL = os.getenv("LLM_MODEL", "gemma3:1b")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
```

---

## 🟢 Minor Issues & Improvements

### 7. **Missing Docstrings for Class Methods**
**Severity:** Low  
**Impact:** Reduced code documentation

The `FilteredRetriever` class methods have docstrings, but could be more detailed.

### 8. **Magic Numbers** (Line 138, 146)
**Severity:** Low  
**Impact:** Unclear intent

**Current:**
```python
for i, doc in enumerate(retrieved_docs[:5], 1):  # Show first 5
    ...
    st.text(doc.page_content[:400] + "..." if len(doc.page_content) > 400 else doc.page_content)
```

**Recommended:**
```python
MAX_DEBUG_CHUNKS = 5
MAX_CHUNK_PREVIEW_LENGTH = 400

for i, doc in enumerate(retrieved_docs[:MAX_DEBUG_CHUNKS], 1):
    ...
    preview = doc.page_content[:MAX_CHUNK_PREVIEW_LENGTH]
    st.text(preview + "..." if len(doc.page_content) > MAX_CHUNK_PREVIEW_LENGTH else doc.page_content)
```

### 9. **Potential Race Condition in Session State** (Lines 105-108)
**Severity:** Low  
**Impact:** Unlikely but possible in edge cases

**Current:** Multiple `if` statements checking session state.

**Recommended:** Use `setdefault()`:
```python
st.session_state.setdefault("messages", [])
st.session_state.setdefault("chat_history", [])
```

### 10. **Missing Input Validation**
**Severity:** Low  
**Impact:** Could handle edge cases better

**Recommended:** Add validation for empty queries:
```python
if prompt := st.chat_input("Ask a question about Everstorm..."):
    prompt = prompt.strip()
    if not prompt:
        st.warning("Please enter a question.")
        st.stop()
    # ... rest of code
```

### 11. **Inefficient Retrieval** (Line 130)
**Severity:** Low  
**Impact:** Documents retrieved twice (once for debug, once for chain)

**Current:** Documents are retrieved explicitly for debugging, then the chain retrieves them again.

**Note:** This is actually fine since the chain needs to retrieve them anyway, but could be optimized if needed.

### 12. **Missing Logging**
**Severity:** Low  
**Impact:** Difficult to debug production issues

**Recommended:** Add logging for important operations:
```python
import logging

logger = logging.getLogger(__name__)

# In load_chain():
logger.info(f"Loading FAISS index from {FAISS_INDEX_PATH}")

# In query handling:
logger.debug(f"Query: {prompt}, Retrieved {len(retrieved_docs)} documents")
```

---

## ✅ Positive Aspects

1. **Good separation of concerns** - Filtering logic separated into functions
2. **Helpful debug features** - Expandable sections for troubleshooting
3. **Proper use of Streamlit caching** - `@st.cache_resource` for expensive operations
4. **Error handling present** - Try/except blocks in place
5. **Clear variable names** - Code is readable
6. **Good documentation** - Docstrings present where needed
7. **Custom retriever implementation** - Proper inheritance from BaseRetriever

---

## 📋 Recommended Refactoring

### Suggested File Structure:
```
app.py
├── Imports (with updated langchain_community)
├── Constants (configuration values)
├── Helper Functions
│   ├── filter_documents()
│   ├── extract_filename()
│   └── validate_query()
├── FilteredRetriever Class
├── load_chain() Function
└── Streamlit UI Code
```

---

## 🎯 Priority Action Items

1. **HIGH:** Update deprecated LangChain imports
2. **MEDIUM:** Add type hints throughout
3. **MEDIUM:** Extract duplicate filename extraction logic
4. **MEDIUM:** Improve error handling with specific exceptions
5. **MEDIUM:** Move hardcoded values to configuration
6. **LOW:** Add constants for magic numbers
7. **LOW:** Add input validation
8. **LOW:** Add logging

---

## 📊 Code Quality Metrics

- **Lines of Code:** 179
- **Cyclomatic Complexity:** Low (simple linear flow)
- **Code Duplication:** ~10 lines (filename extraction)
- **Test Coverage:** Not applicable (no tests present)
- **Documentation Coverage:** ~60% (missing some function docstrings)

---

## 🔧 Quick Wins (Easy fixes with high impact)

1. Fix redundant `source.lower()` call (1 line change)
2. Extract filename function (reduces duplication)
3. Add constants for magic numbers (improves readability)
4. Use `setdefault()` for session state (cleaner code)

---

## 📝 Notes

- The code works correctly despite the issues listed
- Most issues are maintainability/quality improvements rather than bugs
- The deprecated imports will become breaking changes in future LangChain versions
- Consider adding unit tests for `filter_documents()` and `FilteredRetriever`

---

**End of Code Review**

