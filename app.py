from flask import Flask, render_template, request, redirect, url_for
import requests
from doc import documents  # Importing the documents list from a separate file

app = Flask(__name__)

# Create a mapping of document titles to their Google Doc IDs
document_ids = {}

for document in documents:
    title = document["title"]
    link = document["link"]
    # Extract the document ID from the link
    document_id = link.split('/d/')[1].split('/')[0]
    document_ids[title] = document_id

# Function to fetch data from Google Docs
def fetch_data_from_google_doc(doc_id):
    try:
        url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
        response = requests.get(url)

        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to retrieve data. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"An error occurred: {e}"


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        # Filter documents based on the search keyword
        results = [doc for doc in documents if keyword.lower() in doc['title'].lower()]
        # Render index.html with the filtered documents and all documents
        return render_template('index.html', documents=results, all_documents=documents, search=True)

    # Render the index.html with all documents on a GET request
    return render_template('index.html', documents=[], all_documents=documents, search=False)


@app.route('/')
def home():
    return render_template('home.html')





# Display document content based on title
@app.route('/document/<title>')
def document(title):
    doc_id = document_ids.get(title)
    if doc_id:
        content = fetch_data_from_google_doc(doc_id)
    else:
        content = "Document not found."
    return render_template('display.html', title=title, content=content)

if __name__ == '__main__':
    app.run(debug=True)





