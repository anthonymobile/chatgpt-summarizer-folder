import openai
import os
import PyPDF2
from bs4 import BeautifulSoup

# set up your OpenAI API key
openai.api_key = 'YOUR_API_KEY'

# function to read a PDF file and return its contents as a string
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        contents = ''
        for i in range(reader.getNumPages()):
            contents += reader.getPage(i).extractText()
        return contents

# function to read an HTML file and return its contents as a string
def read_html(file_path):
    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        contents = soup.get_text()
        return contents

# function to summarize text using OpenAI's GPT-3 API
def summarize_text(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=(f"Please summarize the following text:\n{text}\n\nSummary:"),
        temperature=0.5,
        max_tokens=100,
        n=1,
        stop=None,
        timeout=30,
    )
    summary = response.choices[0].text.strip()
    return summary

# main function to read a folder of PDFs and HTML files and summarize their contents
def summarize_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith('.pdf'):
            contents = read_pdf(file_path)
        elif file_name.endswith('.html'):
            contents = read_html(file_path)
        else:
            continue
        summary = summarize_text(contents)
        print(f'Summary of {file_name}: {summary}')

# example usage
summarize_folder('/path/to/folder')
