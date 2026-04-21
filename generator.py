import os
import markdown
from jinja2 import Environment, FileSystemLoader

# Setup folders - Make sure these match your folder names exactly
POSTS_DIR = 'posts'      
OUTPUT_DIR = 'docs'      
TEMPLATE_DIR = 'templates'

# Initialize Jinja2 environment
# This looks inside your /templates folder
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def generate_blog():
    # Create the output folder if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    posts_metadata = []

    # 1. Load the templates
    try:
        post_template = env.get_template('blog_template.html')
        index_template = env.get_template('index_template.html')
    except Exception as e:
        print(f"Error: Could not find templates. Make sure they are in the /{TEMPLATE_DIR} folder.")
        print(f"Details: {e}")
        return

    # 2. Process Markdown files in /posts
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            file_path = os.path.join(POSTS_DIR, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                # Convert Markdown to HTML
                html_content = markdown.markdown(text)
                
                # Create a clean title from the filename
                title = filename.replace('-', ' ').replace('.md', '').title()
                output_filename = filename.replace('.md', '.html')
                
                posts_metadata.append({'title': title, 'url': output_filename})

                # Save the individual blog post page
                output_path = os.path.join(OUTPUT_DIR, output_filename)
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(post_template.render(title=title, content=html_content))

    # 3. Generate the Home Page (index.html)
    index_path = os.path.join(OUTPUT_DIR, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_template.render(posts=posts_metadata))

    print(f"🎉 Success! Your blog was generated in the /{OUTPUT_DIR} folder.")

if __name__ == "__main__":
    generate_blog()