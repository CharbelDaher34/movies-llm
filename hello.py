import json
from bs4 import BeautifulSoup

# Read the HTML content from file
with open("./fine_tune_encoders.ipynb", "r", encoding='utf-8') as file:
    html_content = file.read()

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize Notebook structure
notebook = {
    "cells": [],
    "metadata": {},
    "nbformat": 4,
    "nbformat_minor": 5
}

# Iterate through all relevant tags in order
for element in soup.find_all(['h1', 'h2', 'p', 'pre']):
    if element.name in ['h1', 'h2', 'p']:
        text = element.get_text().strip()
        if not text:
            continue  # Skip empty paragraphs/headings
        if element.name == 'h1':
            markdown = f"# {text}"
        elif element.name == 'h2':
            markdown = f"## {text}"
        else:
            markdown = text
        notebook['cells'].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": markdown.splitlines(keepends=True)
        })
    elif element.name == 'pre':
        # Handle <pre><code> blocks
        code_tag = element.find('code')
        if code_tag:
            code_text = code_tag.get_text()
            notebook['cells'].append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": code_text.splitlines(keepends=True)
            })

# Save as .ipynb file
notebook_path = './fine_tune_encoders_extracted.ipynb'
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print(f"Notebook saved to {notebook_path}")
