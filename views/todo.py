from flask import Blueprint, url_for, redirect, flash, request, render_template, jsonify

from extensions import db
from models.Todo import Todo
from flask_login import current_user

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/todos')
def get_todos():
    todos = Todo.query.all()
    serialized_todos = [{
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'completed': todo.completed
    } for todo in todos]
    return jsonify(serialized_todos)


@todo_bp.route('/')
def show_todos():
    db.create_all()
    if not current_user.is_authenticated:
        return redirect('/login')
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', todos=todos)


@todo_bp.route('/create', methods=['POST'])
def create_todo():
    if not current_user.is_authenticated:
        flash('You must sign in to create tasks')
        return redirect(url_for('todo.show_todos'))

    title = request.form['title']
    description = request.form['description']

    todo = Todo(title=title, description=description, user_id=current_user.id)
    db.session.add(todo)
    db.session.commit()

    return redirect('/')


@todo_bp.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    # retrieve the task with the specified ID from the database
    todo = Todo.query.get_or_404(id)

    # update the completion status of the task based on the form data
    completed = request.form.get('completed', False)
    todo.completed = (completed == 'True')

    # save the changes to the database
    db.session.commit()

    # redirect to the index page
    return redirect(url_for('todo.show_todos'))


@todo_bp.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash('Task successfully deleted!')
    return redirect(url_for('todo.show_todos'))



