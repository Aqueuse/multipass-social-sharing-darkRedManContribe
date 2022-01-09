from passlib.hash import sha256_crypt

from models.socialNetworks import FacebookTask, TwitterTask, InstagramTask
from models import User, BasicTask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///C:\\Users\\jaima\\Desktop\\multipass.db')

database = declarative_base(bind=engine)
database.metadata.create_all()

Session = sessionmaker(bind=engine)
session = Session()


# ------------------ Users ----------------- #

def create_user(email, password):
    encrypted_password = sha256_crypt.hash(password)
    User.create_user(email, encrypted_password)


def create_users_if_not_exist():
    User.create_database_if_not_exist()


def get_user(email):
    user = User.get_user(email)
    return user


def validate_user(email, password):
    user_query = get_user(email)
    if len(user_query) == 0:
        return False
    else:
        stored_password = user_query.password
        if sha256_crypt.verify(password, stored_password):
            return True
    return False


def update_user(email, password):
    User.update_user(email, password)


def delete_user(email):
    User.delete_user(email)


def user_exist(email):
    return User.user_exist(email)


# ------------------ Tasks ----------------- #

def create_basic_task(user_id, name, date, repetition, days, months):
    BasicTask.create_database_if_not_exist()
    task_id = BasicTask.get_max_task_id()+1
    BasicTask.create_basic_task(task_id, user_id, name, date, repetition, days, months)


def delete_basic_task(task_id):
    BasicTask.delete_basic_task(task_id)
    if FacebookTask.facebook_task_exist(task_id):
        FacebookTask.delete_facebook_task(task_id)
    if TwitterTask.twitter_task_exist(task_id):
        TwitterTask.delete_twitter_task(task_id)
    if InstagramTask.instagram_task_exist(task_id):
        InstagramTask.delete_instagram_task(task_id)


def get_user_tasks(user_id):
    basic_tasks = BasicTask.get_user_basic_tasks(user_id)
    for task in basic_tasks:
        task["facebook"] = FacebookTask.get_facebook_task(task.task_id)
        task["twitter"] = TwitterTask.get_twitter_task(task.task_id)
        task["instagram"] = InstagramTask.get_instagram_task(task.task_id)
    return basic_tasks


def get_max_task_id():
    return BasicTask.get_max_task_id()


def get_frequency_sorted_tasks(frequency, tasks):
    print("not implemented")


def get_today_daily_tasks(current_date):
    print("not implemented")


def get_today_weekly_tasks(current_date, current_day):
    print("not implemented")


def get_today_monthly_tasks(current_date, current_day_int, current_month):
    print("not implemented")


def get_today_custom_tasks(current_date, current_day, current_month):
    print("not implemented")

# --------------- log activity -------------- #

# def log_task_resume(user_id, task_id, status):
#     db.log.insert_one({"user_id": user_id, "task_id": task_id, "status": status})
