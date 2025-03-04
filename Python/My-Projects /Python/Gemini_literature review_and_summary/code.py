
import os
import fitz  # PyMuPDF
import requests
import concurrent.futures
import time
import re
import random
from datetime import datetime

# Set up your Gemini API key
GEMINI_API_KEY = "Past_your_API_key_here"

# Default folder for PDFs
DEFAULT_PDF_FOLDER = "papers"

# Output files
SUMMARY_FILE = "literature_review.txt"
FULL_REVIEW_FILE = "full_literature_review.txt"
LOG_FILE = "log.txt"

# Maximum number of pages to process
MAX_PAGES = 20

# Maximum characters to send to Gemini
MAX_TEXT_LENGTH = 10000

# Variations for introductory phrases
INTRO_VARIATIONS = [
    "This study", "The research", "A recent study", "This investigation", 
    "The analysis", "A recent examination", "This work", "The present study"
]

def log_error(message):
    """Log errors to a file."""
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

def extract_text_from_pdf(pdf_path, max_pages=MAX_PAGES):
    """Extract text from a PDF file, limiting the number of pages."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for i, page in enumerate(doc):
            if i >= max_pages:
                break
            text += page.get_text("text") + "\n"
        return text[:MAX_TEXT_LENGTH].strip()
    except Exception as e:
        log_error(f"Error extracting text from {pdf_path}: {e}")
        return None

def summarize_with_gemini(text):
    """Summarize text using Gemini API with retries."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{
                "text": (
                    "Summarize the following paper into a concise literature review entry (4-5 sentences). "
                    "Use a variety of introductory phrases like This study, The research, A recent study, This investigation, "
                    "The analysis, A recent examination, This work, The present study "
                    "to make each summary unique. Focus on the problem, methodology, key findings, and relevance:\n\n" 
                    + text
                )
            }]
        }]
    }

    for attempt in range(3):
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            try:
                result = response.json()
                summary = result['candidates'][0]['content']['parts'][0]['text']
                # Replace a standard phrase with a random variation for variety
                summary = summary.replace("This study", random.choice(INTRO_VARIATIONS), 1)
                return summary
            except KeyError as e:
                log_error(f"KeyError in response: {e}")
                return "Error: Unable to parse summary."
        elif response.status_code == 429:
            wait_time = 2 ** attempt
            log_error(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            log_error(f"API error (status {response.status_code}): {response.text}")
            return "Error: Unable to generate summary."
    return "Error: Failed after multiple attempts."

def extract_citation_from_filename(filename):
    """Extracts author and year from a filename like 'Smith_2020.pdf'."""
    match = re.search(r"([A-Za-z]+)_(\d{4})", filename)
    if match:
        author, year = match.groups()
        return author, year
    return filename.replace(".pdf", ""), "n.d."

def format_citation(author, year, citation_style, citation_number=None):
    """Formats in-text citation based on user-selected style."""
    if citation_style == "APA":
        return f"({author}, {year})"
    elif citation_style == "MLA":
        return f"{author} ({year})"
    elif citation_style == "IEEE":
        return f"[{citation_number}]"
    return f"({author}, {year})"  # Default to APA

def format_bibliography_entry(filename, author, year, citation_style, citation_number):
    """Formats bibliography entry based on user-selected style (fallback method)."""
    title = filename.replace(".pdf", "").replace("_", " ")
    if citation_style == "APA":
        return f"[{citation_number}] {author}. ({year}). {title}."
    elif citation_style == "MLA":
        return f"[{citation_number}] {author}. \"{title}.\" ({year})."
    elif citation_style == "IEEE":
        return f"[{citation_number}] {author}, \"{title}\", {year}."
    return f"[{citation_number}] {author}. ({year}). {title}."

def extract_doi(text):
    """
    Extracts a DOI from text using a regular expression.
    DOI format usually starts with '10.' followed by a series of digits and characters.
    """
    doi_pattern = re.compile(r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b', re.I)
    match = doi_pattern.search(text)
    if match:
        return match.group(0)
    return None

def get_reference_details_from_doi(doi):
    """
    Uses CrossRef API to fetch bibliographic metadata based on the DOI.
    Returns a tuple of (authors, title, year, doi) if successful.
    """
    url = f"https://api.crossref.org/works/{doi}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get('message', {})
            # Join multiple authors (only last names are used here for simplicity)
            authors_list = data.get('author', [])
            authors = ', '.join(author.get('family', 'Unknown') for author in authors_list) if authors_list else "Unknown"
            title_list = data.get('title', [])
            title = title_list[0] if title_list else "No Title"
            date_parts = data.get('issued', {}).get('date-parts', [[None]])
            year = date_parts[0][0] if date_parts[0][0] else "n.d."
            return authors, title, year, doi
        else:
            log_error(f"CrossRef API error for DOI {doi}: {response.status_code}")
            return None
    except Exception as e:
        log_error(f"Error fetching metadata for DOI {doi}: {e}")
        return None

def process_pdf(pdf_path, citation_style, citation_number):
    """Extract text, summarize, and generate results for a single PDF."""
    filename = os.path.basename(pdf_path)
    print(f"Processing: {filename}")

    text = extract_text_from_pdf(pdf_path)
    if not text:
        return None

    summary = summarize_with_gemini(text)
    
    # Try to extract DOI from the PDF text
    doi = extract_doi(text)
    if doi:
        ref_details = get_reference_details_from_doi(doi)
    else:
        ref_details = None

    if ref_details:
        authors, title, year, doi_used = ref_details
        # Format the bibliography entry with the DOI information
        bib_entry = f"[{citation_number}] {authors}. \"{title}\", {year}. DOI: {doi_used}."
        # Use the first author for in-text citation (split in case of multiple names)
        first_author = authors.split(',')[0]
        in_text_citation = format_citation(first_author, year, citation_style, citation_number)
    else:
        # Fallback to extraction based on filename
        author, year = extract_citation_from_filename(filename)
        bib_entry = format_bibliography_entry(filename, author, year, citation_style, citation_number)
        in_text_citation = format_citation(author, year, citation_style, citation_number)

    # Create in-text summary entry
    entry = f"{summary} {in_text_citation}\n"

    # Append entry to the summary file
    with open(SUMMARY_FILE, "a", encoding="utf-8") as result_file:
        result_file.write(f"{entry}\n")

    return entry, bib_entry

def generate_structured_review_with_gemini():
    """
    Reads the literature_review.txt file and uses the Gemini API to generate a structured
    literature review in the style of a research paper, then saves the result to full_literature_review.txt.
    
    The prompt instructs the API to include a header, a numbered list of literature review entries,
    and a bibliography section with properly formatted references.
    """
    try:
        with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
            literature_text = f.read()
    except Exception as e:
        log_error(f"Error reading {SUMMARY_FILE}: {e}")
        return

    prompt = (
        "You are an expert academic writer. Using the following literature review entries, generate a structured literature review in the format of a research paper. "
        "Include a header with the title 'LITERATURE REVIEW', the current date, a numbered list of literature review entries, and a bibliography section with properly formatted references. "
        "Ensure that the review is cohesive, professional, and follows academic conventions. Make it as paragprahs with no bullets, with intriduction and concluison. \n\n"
        "Literature Review Entries:\n" + literature_text
    )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }

    for attempt in range(3):
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            try:
                result = response.json()
                final_review = result['candidates'][0]['content']['parts'][0]['text']
                with open(FULL_REVIEW_FILE, "w", encoding="utf-8") as f:
                    f.write(final_review)
                print("\nStructured literature review generated and saved to", FULL_REVIEW_FILE)
                return final_review
            except KeyError as e:
                log_error(f"KeyError in final review response: {e}")
                return "Error: Unable to parse final literature review."
        elif response.status_code == 429:
            wait_time = 2 ** attempt
            log_error(f"Rate limit exceeded in final review generation. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            log_error(f"API error (status {response.status_code}) in final review generation: {response.text}")
            return "Error: Unable to generate final literature review."
    return "Error: Failed after multiple attempts."

def main():
    """Main function to process all PDFs and generate the final structured literature review using Gemini."""
    #pdf_folder = input(f"Enter PDF folder path (default: {DEFAULT_PDF_FOLDER}): ").strip() or DEFAULT_PDF_FOLDER
    pdf_folder ='papers'
    if not os.path.exists(pdf_folder):
        print(f"Error: Folder '{pdf_folder}' does not exist.")
        return

    #citation_style = input("Choose citation style (APA, MLA, IEEE): ").strip().upper()'
    citation_style ='IEEE' 

    if citation_style not in ["APA", "MLA", "IEEE"]:
        print("Invalid citation style. Defaulting to APA.")
        citation_style = "APA"

    pdf_files = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

    if not pdf_files:
        print("No PDFs found in the folder.")
        return

    # Clear previous output files
    open(SUMMARY_FILE, "w", encoding="utf-8").close()
    open(LOG_FILE, "w", encoding="utf-8").close()

    print(f"Found {len(pdf_files)} PDFs. Processing...")

    entries = []
    bibliography = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda i: process_pdf(pdf_files[i], citation_style, i+1), range(len(pdf_files))))
    
    for result in results:
        if result:
            entries.append(result[0].strip())
            bibliography.append(result[1].strip())

    # Optionally, you might want to combine the bibliography entries into the literature_review.txt file
    # so that they can be incorporated in the final structured review.
    with open(SUMMARY_FILE, "a", encoding="utf-8") as summary_file:
        summary_file.write("\nBibliography:\n")
        for entry in bibliography:
            summary_file.write(entry + "\n")

    # Generate the structured literature review using Gemini
    generate_structured_review_with_gemini()
    print("\nProcessing complete!")

if __name__ == "__main__":
    main()
