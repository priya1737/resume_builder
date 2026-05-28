import argparse
import threading
import webbrowser
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resume_data = None

    if request.method == 'POST':
        resume_data = {
            'name': request.form.get('name', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'summary': request.form.get('summary', '').strip(),
            'skills': [skill.strip() for skill in request.form.get('skills', '').split('\n') if skill.strip()],
            'experience': [item.strip() for item in request.form.get('experience', '').split('\n') if item.strip()],
            'education': [item.strip() for item in request.form.get('education', '').split('\n') if item.strip()],
            'projects': [item.strip() for item in request.form.get('projects', '').split('\n') if item.strip()],
        }

    return render_template('index.html', resume_data=resume_data)

def render_resume_html(resume_data, filename='resume_output.html'):
    with app.app_context():
        resume_html = render_template('resume.html', resume_data=resume_data)

    # Read CSS
    css_path = 'static/style.css'
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except FileNotFoundError:
        css_content = ''

    # Full HTML with inlined CSS
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume - {resume_data.get('name', 'Resume')}</title>
    <style>
{css_content}
    </style>
</head>
<body>
    <div class="app-shell">
        {resume_html}
    </div>
</body>
</html>"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(full_html)

    import os
    full_path = os.path.abspath(filename)
    file_url = 'file://' + full_path.replace('\\', '/')
    print(f'Generated resume output: {filename}')
    print(f'Full path: {full_path}')
    print(f'Open in browser: {file_url}')
    
    # Auto-open in browser
    webbrowser.open(file_url)
    
    return filename


def prompt_resume_data():
    print('Enter resume details:')
    name = input('Full Name: ').strip()
    email = input('Email: ').strip()
    phone = input('Phone: ').strip()
    summary = input('Professional Summary: ').strip()

    def prompt_lines(prompt_text):
        print(f'{prompt_text} (enter blank line to finish):')
        lines = []
        while True:
            line = input().strip()
            if not line:
                break
            lines.append(line)
        return lines

    skills = prompt_lines('Skills')
    experience = prompt_lines('Experience')
    education = prompt_lines('Education')
    projects = prompt_lines('Projects')

    return {
        'name': name,
        'email': email,
        'phone': phone,
        'summary': summary,
        'skills': skills,
        'experience': experience,
        'education': education,
        'projects': projects,
    }


def open_browser():
    webbrowser.open('http://127.0.0.1:5000')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resume builder')
    parser.add_argument('--web', action='store_true', help='Start web app in browser')
    parser.add_argument('--output', default='resume_output.html', help='Output HTML file path for CLI mode')
    args = parser.parse_args()

    if args.web:
        threading.Timer(1.0, open_browser).start()
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    else:
        resume_data = prompt_resume_data()
        render_resume_html(resume_data, filename=args.output)
