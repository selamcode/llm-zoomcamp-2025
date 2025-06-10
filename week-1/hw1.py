import requests

# URL of the JSON file hosted on GitHub (contains all courses and their FAQ documents)
docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'

# Send an HTTP GET request to fetch the JSON data from the URL
docs_response = requests.get(docs_url)

# Parse the JSON response into a Python list (each item = a course with documents)
documents_raw = docs_response.json()

# 📂 This will store the final flattened list of documents (one item per FAQ)
documents = []

# course and 'course' are different, course is a variable here, 'course' a key in our json

# 🔁 Loop through each course and its documents (the first list in the structure -> ['course', 'documents'])
for course in documents_raw:
    course_name = course['course']  # Get the name of the course (e.g., "ml-zoomcamp")

    # 🔁 For every documents (question/answer) in the course {questionn, text, secion}
    for doc in course['documents']:
        doc['course'] = course_name  # Add the course name to each document
        documents.append(doc)        # Store the enriched document in the final list

# 🖨️ Print the first document to see the structure
print(documents[0])
