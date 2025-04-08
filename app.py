from flask import Flask, jsonify, render_template
import os
import json


def load_form_templates():
    json_file = "forms.json"  # Name of your single JSON file
    templates = {}
    
    # Check if the JSON file exists
    if not os.path.exists(json_file):
        # Create an empty JSON file if it doesn't exist
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({}, f)  # Initialize with empty dict
        return templates  # Return empty dict for new files
    
    # Load data from the JSON file
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            templates = json.load(f)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in forms.json. Returning empty templates.")
        templates = {}
    
    return templates

app = Flask(__name__)

    

FORM_TEMPLATES = load_form_templates()

@app.route('/')
def index():
    return render_template('homePage.html')  # Your main HTML file
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/forms')
def get_forms_list():
    # Return simplified list for selection page
    form_list = [{
        'id': form_id,
        'title': data['title'],
        'description': data['description'],
        'category': data.get('category', 'general'),
        'downloads': data.get('downloads', 0)
    } for form_id, data in FORM_TEMPLATES.items()]
    return jsonify(form_list)

@app.route('/api/forms/<form_id>')
def get_form_template(form_id):
    if form_id not in FORM_TEMPLATES:
        return jsonify({'error': 'Form not found'}), 404
    return jsonify(FORM_TEMPLATES[form_id])

@app.route('/api/save-form', methods=['POST'])
def save_form():
    data = request.json
    # Save to database or file system
    print("Form data received:", data)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)