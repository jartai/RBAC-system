# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from tables import User, GroupActions, Group, Action, LoggedUsers, metadata

checkPassword = lambda pass_true, pass_typed: pass_true == pass_typed

class return_status:
    ok = 1
    fault = 2
    invalid_login_or_password = 3
    user_not_login = 4


class Manage(object):
    @classmethod
    def connect(self, engine_str, engine_args={}, session_args={}):
        self.initEngine(engine_str, **engine_args)
        self.initSession(**session_args)
        self.initTables()
        return self

    @classmethod
    def initSession(self, **kwargs):
        self.session = sessionmaker(bind=self.engine, **kwargs)()

    @classmethod
    def initEngine(self, engine_string, **kwargs):
        self.engine = create_engine(engine_string, **kwargs)

    @classmethod
    def initTables(self):
        metadata.create_all(self.engine)

    @classmethod
    def commit(self):
        try:
            Manage.session.commit()
        except IntegrityError as err:
            Manage.session.rollback()
            print err

    class Groups(object):
        @classmethod
        def add(self, name):
            Manage.session.add(Group(name))
            self.commit()

    class Users(object):
        @classmethod
        def add(self, name, lastname, patronymic, login, password, group):
            if isinstance(group, str) or isinstance(group, unicode):
                group = Manage.session.query(Group).filter(Group.name == group).first().id
            Manage.session.add(User(name, lastname, patronymic, login, password, group))
            self.commit()

        @classmethod
        def login(self, login, password):
            # TODO Надо проверить, а может юзер уже залоген
            user = Manage.session.query(User).filter(User.login == login).first()
            if user and checkPassword(user.password, password):
                loggedUser = LoggedUsers(user.id)
                Manage.session.add(loggedUser)
                self.commit()
            else:
                print "User with this login='{}' and password doesnt exists".format(login)
                return return_status.invalid_login_or_password

        @classmethod
        def logout(self, user):
            maybe_loggedUser = Manage.session.query(LoggedUsers).filter(LoggedUsers.user == user).first()
            if maybe_loggedUser:
                Manage.session.delete(maybe_loggedUser)
                self.commit()
                return True
