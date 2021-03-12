from functools import reduce

import bcrypt

import common
from psycopg2.extras import RealDictCursor
import datetime


def get_submission_time():
    time = datetime.datetime.now()
    return time.strftime('%Y-%m-%d %H:%M:%S')


@common.connection_handler
def get_all_questions(cursor: RealDictCursor):
    query = """
    SELECT * FROM question
    ORDER BY submission_time
    """
    cursor.execute(query)
    return cursor.fetchall()


@common.connection_handler
def get_all_questions(cursor: RealDictCursor, order_by, order):
    query = f"""
    SELECT * FROM question
    ORDER BY {order_by} {order};
    """
    cursor.execute(query)
    return cursor.fetchall()


@common.connection_handler
def get_all_answers(cursor: RealDictCursor):
    query = """
    SELECT * FROM answer
    ORDER BY submission_time
    """
    cursor.execute(query)
    return cursor.fetchall()


@common.connection_handler
def get_question_by_id(cursor: RealDictCursor, id: int):
    query = """
    SELECT * FROM question
    WHERE id=%(id)s
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchone()


@common.connection_handler
def get_answer_by_id(cursor: RealDictCursor, id: int):
    query = """
    SELECT * FROM answer
    WHERE id=%(id)s
    ORDER BY submission_time
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchone()


@common.connection_handler
def get_answers_by_question_id(cursor: RealDictCursor, id: int):
    query = """
    SELECT * FROM answer
    WHERE question_id=%(id)s
    ORDER BY submission_time
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()


@common.connection_handler
def insert_question_to_database(cursor: RealDictCursor, question: dict):
    query = """
            INSERT INTO question (user_id, submission_time, title, message, vote_number, view_number)
            VALUES (%(user_id)s, %(submission_time)s, %(title)s, %(message)s, %(vote_number)s, %(view_number)s);
            """
    cursor.execute(query, {
        'user_id': question['user_id'],
        'submission_time': question['submission_time'],
        'message': question['message'],
        'title': question['title'],
        'vote_number': question['vote_number'],
        'view_number': question['view_number'],
    })
    return "QUESTION ADDED"


@common.connection_handler
def insert_answer_to_database(cursor: RealDictCursor, answer: dict):
    query = """
               INSERT INTO answer (user_id, submission_time, vote_number, question_id, message, image)
               VALUES (%(user_id)s, %(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s)
               """
    cursor.execute(query, {
        'user_id': answer['user_id'],
        'submission_time': answer['submission_time'],
        'vote_number': answer['vote_number'],
        'question_id': answer['question_id'],
        'message': answer['message'],
        'image': answer['image']
    })
    return "ANSWER ADDED"


@common.connection_handler
def delete_question_from_database(cursor: RealDictCursor, id: int):
    query = """
    DELETE FROM question
    WHERE id=%(id)s
    """
    cursor.execute(query, {'id': id})
    return "QUESTION DELETED"


@common.connection_handler
def delete_answer_from_database(cursor: RealDictCursor, id: int):
    query = """
    DELETE FROM answer
    WHERE id=%(id)s
    """
    cursor.execute(query, {'id': id})
    return "ANSWER DELETED"


@common.connection_handler
def delete_comment_from_database(cursor: RealDictCursor, id: int):
    query = """
    DELETE FROM comment
    WHERE id=%(id)s
    """
    cursor.execute(query, {'id': id})
    return "COMMENT DELETED"


@common.connection_handler
def update_question_in_database(cursor: RealDictCursor, title: str, message: str, id: int):
    query = """
    UPDATE question
    SET title = %(title)s, message = %(message)s
    WHERE id=%(id)s
    """
    cursor.execute(query, {'title': title, 'message': message, 'id': id})
    return "QUESTION UPDATED"


@common.connection_handler
def update_answer_in_database(cursor: RealDictCursor, message: str, id: int):
    query = """
    UPDATE answer
    SET submission_time = %(submission_time)s, message = %(message)s
    WHERE id=%(id)s
    """
    cursor.execute(query, {'message': message, 'id': id, 'submission_time': get_submission_time()})
    return "ANSWER UPDATED"


@common.connection_handler
def update_comment_in_database(cursor: RealDictCursor, message: str, id: int) -> list:
    query = """
     UPDATE comment
     SET submission_time = %(submission_time)s, message = %(message)s, edited_count = edited_count + 1
     WHERE id=%(id)s
     """
    cursor.execute(query, {'message': message, 'id': id, 'submission_time': get_submission_time()})
    return "COMMENT UPDATED"


@common.connection_handler
def get_vote_number_question(cursor: RealDictCursor, id: int):
    query = """
    SELECT vote_number FROM question
    WHERE id=%(id)s
    """
    cursor.execute(query, {'id': id})
    vote_number = cursor.fetchall()
    return vote_number[0]


@common.connection_handler
def get_vote_number_answer(cursor: RealDictCursor, id: int):
    query = """
    SELECT vote_number FROM answer
    WHERE id=%(id)s
    """
    cursor.execute(query, {'id': id})
    vote_number = cursor.fetchall()
    return vote_number[0]


@common.connection_handler
def update_vote_number_question(cursor: RealDictCursor, vote_number, id: int):
    query = """
    UPDATE question
    SET vote_number = %(vote_number)s
    WHERE id = %(id)s
    """
    cursor.execute(query, {'vote_number': vote_number, 'id': id})
    return "VOTE NUMBER UPDATED"


@common.connection_handler
def update_vote_number_answer(cursor: RealDictCursor, vote_number, id: int):
    query = """
    UPDATE answer
    SET vote_number = %(vote_number)s
    WHERE id = %(id)s
    """
    cursor.execute(query, {'vote_number': vote_number, 'id': id})
    return "VOTE NUMBER UPDATED"


@common.connection_handler
def get_comment_for_question(cursor: RealDictCursor, question_id):
    query = """
    SELECT * FROM comment
    WHERE question_id=%(question_id)s
    and answer_id is null
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@common.connection_handler
def insert_comment_question_to_database(cursor: RealDictCursor, comment_to_question: dict):
    query = """
    INSERT INTO comment(user_id, question_id, answer_id, message, submission_time, edited_count)
    VALUES (%(user_id)s, %(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s)
    """
    cursor.execute(query, {
        'user_id': comment_to_question['user_id'],
        'question_id': comment_to_question['question_id'],
        'answer_id': comment_to_question['answer_id'],
        'message': comment_to_question['message'],
        'submission_time': comment_to_question['submission_time'],
        'edited_count': comment_to_question['edited_count']
    })
    return "COMMENT ADDED"


@common.connection_handler
def get_comment_for_answer(cursor: RealDictCursor, question_id):
    query = """
    SELECT * FROM comment
    WHERE answer_id is NOT null
    and question_id = %(question_id)s
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@common.connection_handler
def get_comment_by_id(cursor: RealDictCursor, comment_id: int):
    query = """
    SELECT * FROM comment
    WHERE id = %(comment_id)s
    """
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchone()


@common.connection_handler
def insert_comment_answer_to_database(cursor: RealDictCursor, new_comment: dict):
    query = """
    INSERT INTO comment(user_id, question_id, answer_id, message, submission_time, edited_count)
    VALUES (%(user_id)s, %(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s)
    """
    cursor.execute(query, {
        'user_id': new_comment['user_id'],
        'question_id': new_comment['question_id'],
        'answer_id': new_comment['answer_id'],
        'message': new_comment['message'],
        'submission_time': new_comment['submission_time'],
        'edited_count': new_comment['edited_count']
    })
    return "COMMENT ADDED"


@common.connection_handler
def get_five_latest_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time DESC
                    LIMIT 5;
                    """)
    questions = cursor.fetchall()
    return questions


@common.connection_handler
def get_question_by_phrase(cursor, phrase):
    cursor.execute("""
                            SELECT * FROM question
                            WHERE LOWER(title) LIKE LOWER(%(phrase)s) 
                            OR LOWER(message) LIKE LOWER(%(phrase)s);
                            """,
                   {'phrase': '%' + phrase + '%'})
    return cursor.fetchall()


@common.connection_handler
def insert_question_tag_to_database(cursor: RealDictCursor, new_tag: dict):
    query = """
        INSERT INTO tag(name)
        VALUES (%(name)s)
        """
    cursor.execute(query, {'name': new_tag['name']})
    return "TAG HAS BEEN ADDED"


@common.connection_handler
def get_all_tags(cursor: RealDictCursor):
    query = """
    SELECT * FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()


@common.connection_handler
def insert_association_to_tag(cursor: RealDictCursor, tags_for_question: dict):
    query = '''
        INSERT INTO question_tag(question_id, tag_id)
        VALUES (%(question_id)s, %(tag_id)s)
    '''
    cursor.execute(query, {
        'question_id': tags_for_question['question_id'],
        'tag_id': tags_for_question['tag_id']
    })
    return "you have assigned a tag to the question"


@common.connection_handler
def get_tags_for_question(cursor: RealDictCursor, question_id: int):
    query = """
    SELECT * FROM tag JOIN question_tag ON tag.id = question_tag.tag_id WHERE question_id=%(question_id)s
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@common.connection_handler
def delete_tag_for_question(cursor: RealDictCursor, tags_for_delete: dict):
    query = '''
    DELETE FROM question_tag
    WHERE tag_id = %(tag_id)s AND question_id = %(question_id)s
    '''
    cursor.execute(query, {'question_id': tags_for_delete['question_id'], 'tag_id': tags_for_delete['tag_id']})
    return 'tag has been deleted'


@common.connection_handler
def get_question_by_phrase(cursor, phrase):
    cursor.execute("""
                            SELECT * FROM question
                            WHERE LOWER(title) LIKE LOWER(%(phrase)s) 
                            OR LOWER(message) LIKE LOWER(%(phrase)s);
                            """,
                   {'phrase': '%' + phrase + '%'})
    return cursor.fetchall()


@common.connection_handler
def check_username_exists(cursor: RealDictCursor, username: str):
    query = """
        SELECT * FROM users
        WHERE username = %(username)s;
         """
    cursor.execute(query, {
        'username': username
    })
    return cursor.fetchone()


@common.connection_handler
def register_user(cursor: RealDictCursor, username: str, seen_password: str, submission_time: int):
    if check_username_exists(username):
        return False
    query = """
    INSERT INTO users (username, password, submission_time, count_questions, count_answers, count_comments, reputation)
    VALUES (%(username)s, %(password)s, %(submission_time)s, 0, 0, 0, 0)
           """
    return cursor.execute(query, {
        'username': username,
        'password': encrypt_password(seen_password),
        'submission_time': submission_time
    })


def encrypt_password(password):
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pass.decode('utf-8')


@common.connection_handler
def check_user(cursor: RealDictCursor, username: str):
    query = """
        SELECT id, password
        FROM users
        WHERE username ILIKE %(username)s;
    """
    cursor.execute(query, {'username': username})
    return cursor.fetchone()


def verify_password(text_password, hashed_pass):
    return bcrypt.checkpw(text_password.encode('utf-8'), hashed_pass.encode('utf-8'))


@common.connection_handler
def users_data(cursor: RealDictCursor):
    query = """
        SELECT *
        FROM users
            """
    cursor.execute(query)
    return cursor.fetchall()


@common.connection_handler
def get_questions_by_user_id(cursor: RealDictCursor, user_id: int):
    query = """
            SELECT id, submission_time, view_number, vote_number, title, message, image
            FROM question
            WHERE user_id = %(user_id)s
    """
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@common.connection_handler
def get_answers_for_question_user_id(cursor: RealDictCursor, user_id: int):
    query = """ SELECT answer.*, question.id, question.title
            FROM answer
            LEFT JOIN question
            ON answer.question_id = question.id
            WHERE answer.user_id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@common.connection_handler
def get_comments_for_question_user_id(cursor: RealDictCursor, user_id: int):
    query = """
                SELECT comment.*, question.id, question.title
                FROM comment
                LEFT JOIN question
                ON comment.question_id = question.id
                WHERE comment.user_id = %(user_id)s AND comment.answer_id IS NULL 
        """
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@common.connection_handler
def update_question_count(cursor: RealDictCursor, user_id: int):
    query = """
        UPDATE users
        SET count_questions = count_questions + 1
        WHERE id = %(user_id)s
        """
    return cursor.execute(query, {'user_id': user_id})


@common.connection_handler
def update_answer_count(cursor: RealDictCursor, user_id: int):
    query = """
        UPDATE users
        SET count_answers = count_answers + 1
        WHERE id = %(user_id)s
        """
    return cursor.execute(query, {'user_id': user_id})


@common.connection_handler
def update_comment_count(cursor: RealDictCursor, user_id: int):
    query = """
        UPDATE users
        SET count_comments = count_comments + 1
        WHERE id = %(user_id)s
        """
    return cursor.execute(query, {'user_id': user_id})


@common.connection_handler
def show_all_tags(cursor: RealDictCursor):
    query = """
               SELECT tag.name, count(question_tag.question_id) as question_number
               FROM question_tag JOIN tag
               ON question_tag.tag_id=tag.id
               GROUP BY tag.name
               """
    cursor.execute(query)
    return cursor.fetchall()


# @common.connection_handler
# def valid_answer(cursor: RealDictCursor, validation: bool, id: int):
#     query = """
#                UPDATE answer
#                SET validation = %(validation)s
#                WHERE id = %(id)s
#                """
#     cursor.execute(query, {
#         'validation': validation,
#         'id': id})
#     return "VALIDATED"
