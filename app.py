from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load novels from a JSON file
def load_novels(filename='novels.json'):
    try:
        with open(filename, 'r') as file:
            novels = json.load(file)
            return novels
    except FileNotFoundError:
        return []

# Save novels to a JSON file
def save_novels(novels, filename='novels.json'):
    with open(filename, 'w') as file:
        json.dump(novels, file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_novel', methods=['GET', 'POST'])
def add_novel():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        description = request.form['description']
        
        novels = load_novels()
        novels.append({
            'title': title,
            'author': author,
            'genre': genre,
            'description': description
        })
        save_novels(novels)
        
        return redirect(url_for('novels'))
    
    return render_template('add_novel.html')

@app.route('/novels')
def novels():
    novels = load_novels()
    return render_template('novels.html', novels=novels)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    novels = load_novels()
    filtered_novels = [novel for novel in novels if query.lower() in novel['title'].lower() or query.lower() in novel['author'].lower()]
    return render_template('novels.html', novels=filtered_novels)

if __name__ == '__main__':
    app.run(debug=True)