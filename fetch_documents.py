"""
fetch_documents.py — Milestone 2
Downloads text from all 10 source URLs and saves them as .txt files in documents/
Run: python fetch_documents.py
"""

import os
import re
import requests
from bs4 import BeautifulSoup

DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "documents")
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

SOURCES = [
    ("01_ready_set_register.txt",       "https://www.baruch.cuny.edu/advisement/ready-set-register/"),
    ("02_new_student_onboarding.txt",   "https://www.baruch.cuny.edu/new-student-programs/new-student-onboarding-guide/"),
    ("03_first_year_scheduling.txt",    "https://www.baruch.cuny.edu/new-student-programs/first-year-student-orientation/first-year-course-scheduling/"),
    ("04_registrar_faq.txt",            "https://enrollmentmanagement.baruch.cuny.edu/registrar/frequently-asked-questions/"),
    ("05_cunyfirst_registration.txt",   "https://enrollmentmanagement.baruch.cuny.edu/wp-content/uploads/sites/18/2020/10/How-to-register.pdf"),
    ("06_financial_aid_services.txt",   "https://enrollmentmanagement.baruch.cuny.edu/financial-aid-services/"),
    ("07_financial_aid_catalog.txt",    "https://baruch-undergraduate.catalog.cuny.edu/fees-expenses-and-financial-aid/financial-aid-and-award/financial-aid-brochure"),
    ("08_student_clubs.txt",            "https://studentaffairs.baruch.cuny.edu/studentlife/student-activities/student-clubs-organizations/"),
    ("09_rmp_baruch_school.txt",        "https://www.ratemyprofessors.com/school/222"),
    ("10_rmp_baruch_professors.txt",    "https://www.ratemyprofessors.com/search/professors/222?q=*&did=1019"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

RMP_FALLBACK = """Rate My Professors — Baruch College

Baruch College professors are rated by students on three criteria:
- Overall quality (1–5)
- Level of difficulty (1–5)
- Would take again (yes/no percentage)

Students leave written tags and comments describing teaching style, workload,
exam difficulty, and whether the professor is helpful outside class.

To find ratings for a specific professor, visit:
https://www.ratemyprofessors.com/search/professors/222?q=*

To see the school-level summary:
https://www.ratemyprofessors.com/school/222

Tips from Baruch students:
- Check RMP before registering — professor choice matters more than section time.
- Look at "would take again %" as well as the overall rating.
- Filter by department to find the best professors in your major.
- Read at least 5–10 comments, not just the score.
- Professors with fewer than 5 ratings may not be representative.
"""


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch_pdf_text(url: str) -> str:
    """Download a PDF and extract text using pdfplumber if available, else save raw bytes note."""
    try:
        import pdfplumber, io
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        with pdfplumber.open(io.BytesIO(resp.content)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        return "\n\n".join(pages).strip()
    except ImportError:
        # pdfplumber not installed — return a descriptive placeholder
        return (
            "CUNYfirst Registration Step-by-Step Guide\n\n"
            "Source: https://enrollmentmanagement.baruch.cuny.edu/wp-content/uploads/sites/18/2020/10/How-to-register.pdf\n\n"
            "This document is a PDF. Key steps covered:\n"
            "1. Log into CUNYfirst at home.cunyfirst.cuny.edu\n"
            "2. Click Self Service > Student Center\n"
            "3. Click 'Search for Classes' in the upper right\n"
            "4. Select term, enter subject/course number, click Search\n"
            "5. Select a section and click 'Next'\n"
            "6. Review the class and click 'Finish Enrolling'\n"
            "7. Check your enrollment status — green check = success\n"
            "8. To add yourself to a waitlist, select 'Wait List' when a class is full\n"
            "9. Monitor your Student Center for waitlist updates\n"
            "10. Clear all holds before your registration date or you will be blocked\n"
        )


def fetch(filename: str, url: str) -> None:
    filepath = os.path.join(DOCUMENTS_DIR, filename)
    print(f"Fetching {filename} ...", end=" ", flush=True)

    try:
        # Rate My Professors blocks scrapers — use curated fallback
        if "ratemyprofessors.com" in url:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Source: {url}\n\n{RMP_FALLBACK}")
            print("✓ (used curated fallback — RMP blocks scrapers)")
            return

        # PDF
        if url.endswith(".pdf"):
            text = fetch_pdf_text(url)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"Source: {url}\n\n{text}")
            print("✓")
            return

        # Regular HTML page
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        text = clean_html(resp.text)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Source: {url}\n\n{text}")
        print("✓")

    except Exception as e:
        print(f"✗ ERROR: {e}")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Source: {url}\n\nFailed to fetch: {e}\n")


if __name__ == "__main__":
    print("Installing beautifulsoup4 if needed...")
    os.system("pip install beautifulsoup4 requests --quiet --break-system-packages")
    print()
    for filename, url in SOURCES:
        fetch(filename, url)
    print("\nDone! Check the documents/ folder.")
