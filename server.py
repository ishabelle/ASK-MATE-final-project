import os
from datetime import timedelta, datetime


from flask import Flask, render_template, request, redirect, url_for, session
import util
import connection

app = Flask(__name__)
app.secret_key = (os.urandom(16))
app.permanent_session_lifetime = timedelta(minutes=5)


@app.route("/")
def get_5_latest_questions():
    questions = connection.get_five_latest_questions()
    return render_template("list.html",
                           questions=questions,
                           title="Main page")


@app.route("/list")
def display_questions_list():
    order_by_options = {'submission_time': 'Submission time', 'view_number': 'View number',
                        'vote_number': 'Vote number', 'title': 'Title'}
    order_options = ['DESC', 'ASC']
    order_by = request.args.get('order_by')
    order = request.args.get('order')
    questions_list = util.order_questions(order_by, order)
    return render_template("list.html",
                           questions=questions_list,
                           title="List questions",
                           select_options=order_by_options,
                           order_options=order_options,
                           order_by=order_by,
                           order=order)


@app.route('/question/<question_id>')
def display_single_question(question_id):
    single_question = connection.get_question_by_id(question_id)
    headers = ["ID", "USER ID", "SUBMISSION TIME", "VIEW NUMBER", "VOTE NUMBER", "TITLE", "MESSAGE", "IMAGE"]
    answer_headers = ["ID","USER ID", "SUBMISSION TIME", "VOTE NUMBER", "QUESTION ID", "MESSAGE", "IMAGE"]
    answers_to_single_question = connection.get_answers_by_question_id(question_id)
    comment_to_question = connection.get_comment_for_question(question_id)
    comment_to_answer = connection.get_comment_for_answer(question_id)
    all_tags = connection.get_all_tags()
    tags_assigned_to_question = connection.get_tags_for_question(question_id)
    return render_template('single_question.html', question_id=question_id,
                           single_question=single_question, headers=headers,
                           answer_headers=answer_headers, answers_to_single_question=answers_to_single_question,
                           comment_to_question=comment_to_question, comment_to_answer=comment_to_answer,
                           all_tags=all_tags, tags_assigned_to_question=tags_assigned_to_question)


@app.route('/add_new_question', methods=['POST', 'GET'])
def add_new_question():
    if request.method == 'GET':
        return render_template('add_question.html')
    if request.method == 'POST':
        question = {'submission_time': connection.get_submission_time(), 'view_number': 0,
                    'vote_number': 0, 'title': request.form.get('title'),
                    'message': request.form.get('message'), 'image': None}
        connection.insert_question_to_database(question)
        return redirect(url_for('display_questions_list'))


@app.route('/question/<question_id>/add_new_answer', methods=['POST', 'GET'])
def add_new_answer(question_id):
    if request.method == 'GET':
        return render_template('add_answer.html', question_id=question_id)
    if request.method == 'POST':
        answer = {'submission_time': connection.get_submission_time(), 'vote_number': 0,
                  'question_id': question_id, 'message': request.form.get('message'),
                  'image': request.form.get('image')}
        connection.insert_answer_to_database(answer)
        return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/question/<question_id>/delete', methods=["POST"])
def delete_question(question_id):
    connection.delete_question_from_database(question_id)
    return redirect(url_for('display_questions_list', question_id=question_id))


@app.route('/question/<question_id>/delete', methods=["GET"])
def confirm_delete_question(question_id):
    return render_template("confirm_delete_question.html", question_id=question_id)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    question_id = request.args.get('question_id')
    connection.delete_answer_from_database(answer_id)
    return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/question/<question_id>/edit', methods=["POST", "GET"])
def update_question(question_id):
    if request.method == 'GET':
        title_content = connection.get_question_by_id(question_id)["title"]
        question_content = connection.get_question_by_id(question_id)["message"]
        return render_template('edit_question.html', question_id=question_id, question_content=question_content,
                               title_content=title_content)
    elif request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        connection.update_question_in_database(title, message, question_id)
        return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/answer/<answer_id>/edit', methods=["POST", "GET"])
def update_answer(answer_id):
    if request.method == 'GET':
        answer_content = connection.get_answer_by_id(answer_id)["message"]
        return render_template('edit_answer.html', answer_id=answer_id, answer_content=answer_content)
    elif request.method == 'POST':
        question_id = request.args.get('question_id')
        message = request.form.get('message')
        connection.update_answer_in_database(message, answer_id)
        return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/comment/<comment_id>/edit', methods=["POST", "GET"])
def update_comment(comment_id):
    if request.method == 'GET':
        comment_content = connection.get_comment_by_id(comment_id)["message"]
        return render_template('edit_comment.html', comment_id=comment_id, comment_content=comment_content)
    elif request.method == 'POST':
        question_id = request.args.get('question_id')
        message = request.form.get('message')
        connection.update_comment_in_database(message, comment_id)
        return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id):
    connection.delete_comment_from_database(comment_id)
    question_id = request.args.get('question_id')
    return redirect(url_for('display_single_question', comment_id=comment_id, question_id=question_id))


@app.route('/question/<int:question_id>/vote')
def vote_for_question(question_id):
    vote_type = request.args.get('vote_type')
    vote_number = connection.get_vote_number_question(question_id)
    vote_up_or_down = util.vote_up_or_down(vote_number, vote_type)
    connection.update_vote_number_question(vote_up_or_down, question_id)
    return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/answer/<answer_id>/vote', methods=["GET"])
def vote_for_answer(answer_id):
    question_id = request.args.get('question_id')
    vote_type = request.args.get('vote_type')
    vote_number = connection.get_vote_number_answer(answer_id)
    vote_up_or_down = util.vote_up_or_down(vote_number, vote_type)
    connection.update_vote_number_answer(vote_up_or_down, answer_id)
    return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=["GET", "POST"])
def add_comment_to_question(question_id):
    if request.method == 'GET':
        return render_template('add_comment_for_question.html', question_id=question_id)
    if request.method == 'POST':
        new_comment = {'question_id': question_id, 'answer_id': None,
                       'message': request.form.get('message'), 'submission_time': connection.get_submission_time(),
                       'edited_count': 0}
        connection.insert_comment_question_to_database(new_comment)
    return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/answer/<answer_id>/new-comment', methods=["GET", "POST"])
def add_comment_to_answer(answer_id):
    question_id = request.args.get("question_id")
    if request.method == 'GET':
        return render_template('add_comment_for_answer.html', answer_id=answer_id, question_id=question_id)
    if request.method == 'POST':
        new_comment = {
                    'question_id': question_id,
                    'answer_id': answer_id,
                    'message': request.form.get('message'),
                    'submission_time': connection.get_submission_time(),
                    'edited_count': 0
                    }
        connection.insert_comment_answer_to_database(new_comment)

        return redirect(url_for('display_single_question',
                                question_id=question_id,
                                ))


@app.route('/question/<int:question_id>/new-tag', methods=["GET", "POST"])
def add_tag(question_id: int):
    if request.method == 'GET':
        all_tags = connection.get_all_tags()
        return render_template('create_tag.html', question_id=question_id, all_tags=all_tags)
    if request.method == 'POST':
        new_tag = {'name': request.form.get('tag')}
        connection.insert_question_tag_to_database(new_tag)
        return redirect(url_for('display_single_question', question_id=question_id))


@app.route('/question/<question_id>/link-question-with-tag', methods=["POST"])
def add_connection(question_id):
    tags_for_question = {'question_id': question_id, 'tag_id': request.form.get('tag-id')}
    connection.insert_association_to_tag(tags_for_question)
    return redirect(url_for('display_single_question', question_id=question_id, tags_for_question=tags_for_question))


@app.route('/question/<question_id>', methods=["POST"])
def get_tags_for_question(question_id):
    tags_assigned_to_question = connection.get_tags_for_question(question_id)
    return render_template('single_question.html', question_id=question_id,
                           tags_assigned_to_question=tags_assigned_to_question)


@app.route('/question/<question_id>/delete_tag', methods=["POST"])
def delete_tag(question_id: int):
    tags_for_delete = {'question_id': question_id, 'tag_id': request.form.get('tag-id')}
    connection.delete_tag_for_question(tags_for_delete)
    return redirect(url_for('display_single_question', question_id=question_id, tags_for_delete=tags_for_delete))


@app.route('/search')
def question_list_by_phrase():
    phrase = request.args.get('phrase')
    if phrase:
        questions = connection.get_question_by_phrase(phrase)
    else:
        return redirect(url_for('index'))
    return render_template('list.html', questions=questions)


@app.route('/registration', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for("display_questions_list"))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if connection.register_user(username, password, submission_time) is False:
            print('Not registered')
        connection.register_user(username, password, submission_time)
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('display_questions_list'))
    if request.method == 'POST':
        username = request.form.get('username')
        typed_password = request.form.get('password')
        user = connection.check_user(username)
        if user and connection.verify_password(typed_password, user['password']):
            session['user_id'] = user['id']
            session['username'] = username
            print('User logged in!')
            return redirect('/')
        else:
            print('User or Password do not match')
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'user_id' not in session:
        print('You are not logged in!')
    else:
        session.pop('user_id', None)
        session.pop('username', None)
    return redirect(url_for('display_questions_list'))


@app.route("/users")
def users():
    users_data = connection.users_data()
    return render_template("users.html", users=users_data)


if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(
        host='localhost',
        port=5000,
        debug=True,
    )
