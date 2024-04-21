from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications (optional but recommended)

db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<Task %r>' % self.id

# Comment out the following 2 lines after initialising the table in your database, these lines will only be required again if you are making changes to the table structure
# with app.app_context():
    # db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            tasks = ToDo(content=task_content).query.order_by(ToDo.date_created).all()
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            return 'There was an issue adding your task'

    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an problem deleting that task'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = ToDo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating your task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)
