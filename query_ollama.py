#!/usr/bin/env python3
import argparse
import os
import webbrowser
from string import Template
from urllib.parse import quote
import sys

def find_template(template_name):
    """
    Search for template in multiple locations:
    1. Current working directory's templates folder
    2. Script directory's templates folder
    """
    if not template_name.endswith('.txt'):
        template_name += '.txt'

    # Search paths
    cwd_path = os.path.join(os.getcwd(), 'templates', template_name)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, 'templates', template_name)

    # Try current working directory first
    if os.path.exists(cwd_path):
        return cwd_path
    # Then try script directory
    elif os.path.exists(script_path):
        return script_path
    else:
        print(f"Error: Template '{template_name}' not found in:")
        print(f"  - {os.path.dirname(cwd_path)}")
        print(f"  - {os.path.dirname(script_path)}")
        exit(1)

def read_template(template_name):
    """Read template file from found location."""
    template_path = find_template(template_name)
    try:
        with open(template_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading template: {e}")
        exit(1)

def open_ollama_query(prompt):
    """Open ollama query in default browser."""
    url = f'http://localhost:3000/?q={quote(prompt)}'
    webbrowser.open_new_tab(url)

def main():
    parser = argparse.ArgumentParser(description='Open ollama query in browser with templated prompts')
    parser.add_argument('--template', required=True, help='Template name from templates directory')
    parser.add_argument('--query', required=True, help='Query to insert into template')
    
    args = parser.parse_args()
    
    # Read and process template
    template_content = read_template(args.template)
    template = Template(template_content)
    prompt = template.safe_substitute(query=args.query)
    
    # Open query in browser
    open_ollama_query(prompt)
    print("Query opened in new browser tab")

if __name__ == '__main__':
    main()
