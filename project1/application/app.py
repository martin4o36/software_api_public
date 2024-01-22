from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, LoginManager, logout_user
from models import db, User, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://software:software@database:5432/tues_software'
app.config['SECRET_KEY'] = 'software'
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('sign_in'))


@app.route('/', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('sign_up.html', error='Username already exists. Choose a different one.')
        
        new_user = User(username=username, email=email, user_password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('sign_in'))

    return render_template('sign_up.html')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(username=username, email=email, user_password=password).first()

        if user:
            login_user(user)
            return redirect(url_for('display_tasks'))
        else:
            return render_template('sign_in.html', error='Invalid username or password')

    return render_template('sign_in.html')

@app.route('/tasks')
@login_required
def display_tasks():
    user_tasks = Task.query.filter_by(user=current_user).all()
    return render_template('dashboard.html', tasks=user_tasks)


@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        task_name = request.form['task_name']
        task_description = request.form['task_description']

        new_task = Task(
            task_name=task_name,
            task_description=task_description,
            is_completed=False,
            user=current_user
        )

        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully')

    return redirect(url_for('display_tasks'))


@app.route('/remove_task/<int:task_id>', methods=['POST'])
@login_required
def remove_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user != current_user:
        flash('You do not have permission to remove this task.')
        return redirect(url_for('display_tasks'))

    db.session.delete(task)
    db.session.commit()

    flash('Task removed successfully')
    return redirect(url_for('display_tasks'))


@app.route('/update_task_description/<int:task_id>', methods=['POST'])
@login_required
def update_task_description(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user != current_user:
        flash('You do not have permission to update this task.')
        return redirect(url_for('display_tasks'))

    try:
        task.task_description = request.form['task_description']
        db.session.commit()
        flash('Task description updated successfully')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating task description: {str(e)}', 'error')

    return redirect(url_for('display_tasks'))


@app.route('/update_is_completed/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user != current_user:
        flash('You do not have permission to update this task.')
        return redirect(url_for('display_tasks'))

    try:
        task.is_completed = not task.is_completed
        db.session.commit()
        flash('Task status updated successfully')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating task status: {str(e)}', 'error')

    return redirect(url_for('display_tasks'))


@app.route('/rename_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def rename_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user != current_user:
        flash('You do not have permission to rename this task.')
        return redirect(url_for('display_tasks'))

    if request.method == 'POST':
        new_task_name = request.form['new_task_name']
        task.task_name = new_task_name
        db.session.commit()

        flash('Task renamed successfully')
        return redirect(url_for('display_tasks'))

    return redirect(url_for('display_tasks'))
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)