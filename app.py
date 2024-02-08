# pip install Flask
# pip install Flask-SQLAlchemy

from flask import Flask, request, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')

    tasks = Task.query.all()
    return render_template_string('''
        <!doctype html>
        <html>
        <head><title>To-Do List</title>


<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    .container {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        width: 500px;
        box-sizing: border-box;
    }

    h2 {
        color: #333;
        text-align: center;
    }

    form {
        width: 100%;
        box-sizing: border-box;
    }

    ul {
        list-style: none;
        padding: 0;
        margin-top: 20px; /* Add space between the form and the list */
    }

    ul li {
        background: #eee;
        padding: 10px;
        margin-bottom: 8px;
        border-radius: 4px;
        position: relative;
    }

    ul li a {
        color: red;
        position: absolute;
        right: 10px;
        top: 10px;
        text-decoration: none;
    }

    input[type="text"] {
        width: 300px;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
        margin-right: 10px;
    }

    input[type="submit"] {
        width: 25%;
        padding: 10px;
        border: none;
        border-radius: 4px;
        background-color: #5cb85c;
        color: white;
        cursor: pointer;
    }

    input[type="submit"]:hover {
        background-color: #4cae4c;
    }
</style>



        </head>
        <body>
            <div class="container">
            <h2>To-Do List</h2>
            <form method="post">
                <input type="text" name="content" placeholder="Enter task here">
                <input type="submit" value="Add Task">
            </form>

            <p>
            <h3>Tasks:</h3>
            <ul>
                {% for task in tasks %}
                <li>{{ task.content }} 
                    <a href="/delete/{{ task.id }}">Delete</a>
                </li>
                {% endfor %}
            </ul>
            </p>
            </div>
        </body>
        </html>
    ''', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

