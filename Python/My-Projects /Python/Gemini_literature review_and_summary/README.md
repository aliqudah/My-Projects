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
Install Dependencies:

Install the required Python packages:

bash
Copy
Edit
pip install pymupdf requests
Alternatively, if a requirements.txt file is included:

bash
Copy
Edit
pip install -r requirements.txt
## Configuration
Before running the script, update the following in the main Python file:

Gemini API Key:
Replace the placeholder value in the GEMINI_API_KEY variable with your actual API key.

PDF Folder:
Ensure you have a folder named papers containing the PDF files you wish to process. You can change the folder name by modifying the DEFAULT_PDF_FOLDER variable.

Citation Style:
Adjust the citation_style variable in the main() function to one of the supported styles: "APA", "MLA", or "IEEE".

Processing Limits:
Modify MAX_PAGES and MAX_TEXT_LENGTH as needed to control the amount of text processed from each PDF.

## Usage
Run the script from the command line:

bash
Copy
Edit
python script_name.py
What Happens Under the Hood?
PDF Discovery:
The script scans the specified folder for PDF files.

Text Extraction:
Extracts text from each PDF, up to a defined page and character limit.

Summarization:
Submits extracted text to the Gemini API to produce a brief literature review entry, using varied introductory phrases (e.g., "This study", "A recent examination") to add uniqueness.

Citation and Bibliography Generation:
Attempts to extract a DOI from the text. If found, fetches bibliographic metadata from CrossRef; otherwise, it parses the filename for citation details.

Formats in-text citations and bibliography entries based on the selected citation style.
Final Document Generation:
Combines literature review entries and bibliography into a single, cohesive document saved as full_literature_review.txt.

Error Logging:
Any issues during processing are logged in log.txt for review.

## Customization
Introductory Phrases:
Edit the INTRO_VARIATIONS list to change the variety of phrases used in summary entries.

Citation Formatting:
Modify the format_citation and format_bibliography_entry functions to adjust how citations are displayed.

API Retry Strategy:
Adjust the retry mechanism and backoff timing in the API request functions if needed.

Output File Names:
Change the names of the output files (literature_review.txt, full_literature_review.txt, log.txt) by modifying the corresponding variables.

## Troubleshooting
API Errors or Rate Limits:
Check log.txt for detailed error messages. The script includes retry logic with exponential backoff for handling rate limits.

Missing PDFs or Incorrect Paths:
Ensure that the specified PDF folder exists and contains valid .pdf files.

DOI Extraction Issues:
If the DOI is not detected, the script defaults to extracting citation details from the filename. Verify your PDFs contain recognizable DOI patterns.

Permission Issues:
Make sure you have read and write permissions for the folders and files used by the script.

## Contributing
Contributions are welcome! If you have suggestions, bug fixes, or improvements:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -am 'Add new feature').
Push to your branch (git push origin feature/your-feature).
Open a Pull Request describing your changes.
For major changes, please open an issue first to discuss what you would like to modify.

## License
This project is licensed under the MIT License. See the LICENSE file for detailed information.
