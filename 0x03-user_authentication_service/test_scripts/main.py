#!/usr/bin/env python3
"""
Main file
"""
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import User
from db import DB

# print(User.__tablename__)
#
# for column in User.__table__.columns:
#     print("{}: {}".format(column, column.type))
#

# from user import User

# my_db = DB()
#
# user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
# print(user_1.id)
#
# user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
# print(user_2.id)


# my_db = DB()
#
# user = my_db.add_user("test@test.com", "PwdHashed")
# print(user.id)

# find_user = my_db.find_user_by(email="test@test.com")
# print(find_user.id)
#
# try:
#     find_user = my_db.find_user_by(email="test2@test.com", hashed_password="PwdHashed")
#     print(find_user.id)
# except NoResultFound:
#     print("Not found")
#
# try:
#     find_user = my_db.find_user_by(no_email="test@test.com")
#     print(find_user.id)
# except InvalidRequestError:
#     print("Invalid")

# my_db.update_user(user.id, hashed_password='NewPwd')
# print("Password updated")

# from auth import _hash_password
#
# print(_hash_password("Hello Holberton").decode('utf-8'))

from auth import Auth

# email = 'me@me.com'
# password = 'mySecuredPwd'
#
# auth = Auth()
#
# try:
#     user = auth.register_user(email, password)
#     print("successfully created a new user!")
# except ValueError as err:
#     print("could not create a new user: {}".format(err))
#
# try:
#     user = auth.register_user(email, password)
#     print("successfully created a new user!")
# except ValueError as err:
#     print("could not create a new user: {}".format(err))


email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

user = auth.register_user(email, password)

# print(auth.valid_login(email, password))
#
# print(auth.valid_login(email, "WrongPwd"))
#
# print(auth.valid_login("unknown@email", password))

# print(auth.create_session(email))
# print(auth.create_session("unknown@email.com"))

# auth.destroy_session(user.id)

# print(user.session_id)

print(auth.get_reset_password_token(email))
print(user.reset_token)
# auth.get_reset_password_token('<PASSWORD>')
