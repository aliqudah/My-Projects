# Automated Literature Review Generator

An all-in-one tool that transforms your collection of research paper PDFs into a polished, structured literature review. This project leverages advanced text extraction, automated summarization, and bibliographic metadata retrieval to help you quickly generate professional literature review entries complete with citations and a comprehensive bibliography.

> **Note:** This tool uses the Gemini API for text summarization and the CrossRef API for DOI metadata lookup. Ensure you have valid API keys and comply with their usage policies.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **PDF Text Extraction:**  
  Uses [PyMuPDF](https://pymupdf.readthedocs.io/) to extract text from PDFs, processing up to a configurable number of pages per document.

- **Automated Summarization:**  
  Utilizes the Gemini API to generate concise, unique summaries of each paper. Each summary is enhanced with varied introductory phrases for a natural flow.

- **Bibliographic Metadata Retrieval:**  
  Automatically extracts DOIs from PDF texts and fetches corresponding metadata from the CrossRef API. Falls back on filename parsing (e.g., `Smith_2020.pdf`) if no DOI is found.

- **Multiple Citation Styles:**  
  Supports APA, MLA, and IEEE citation formats for both in-text citations and bibliography entries.

- **Concurrent Processing:**  
  Processes multiple PDFs concurrently using Python’s `concurrent.futures`, speeding up the literature review generation.

- **Structured Final Output:**  
  Produces a complete literature review document with a header, numbered literature review entries, and a bibliography section. The final document is saved as `full_literature_review.txt`.

- **Robust Error Handling:**  
  Implements retries with exponential backoff for API calls and logs errors to `log.txt` for troubleshooting.

---

## Prerequisites

- **Python Version:**  
  Python 3.6 or higher.

- **API Keys:**  
  - Gemini API Key for text summarization.  
  - (Optional) Access to the CrossRef API for DOI metadata lookup.

- **Dependencies:**  
  - [PyMuPDF](https://pymupdf.readthedocs.io/)  
  - [requests](https://docs.python-requests.org/)  
  - Other standard libraries: `os`, `concurrent.futures`, `time`, `re`, `random`, `datetime`

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/automated-literature-review-generator.git
   cd automated-literature-review-generator
