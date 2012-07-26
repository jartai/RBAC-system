# -*- coding: utf-8 -*-

from sqlalchemy import MetaData, Table, Column, Integer, String, Unicode, ForeignKey
from sqlalchemy.orm import mapper

metadata = MetaData()

actions_table = Table('actions', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(50), unique=True),
    mysql_engine='InnoDB',
    mysql_charset='utf8'

)

groups_table = Table('groups', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(50), unique=True),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

groupsActions_table = Table('groups_actions', metadata,
    Column('id', Integer, primary_key=True),
    Column('guid', Integer, ForeignKey('groups.id')),
    Column('action', Integer, ForeignKey('actions.id')),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode(50)),
    Column('lastname', Unicode(50), server_default=''),
    Column('patronymic', Unicode(50), server_default=''),
    Column('login', String(50), unique=True),
    Column('password', String(50)),
    Column('guid', Integer, ForeignKey('groups.id')),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

loggedUsers_table = Table('logged_users', metadata,
    Column('user', Integer, ForeignKey('users.id'), unique=True),
    mysql_engine='MEMORY',
)


class rep(object):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "<{}('{}')>".format(self.__class__.__name__, self.name)

class Action(rep): pass
class Group(rep): pass
class GroupActions(object): pass

class User(object):
    def __init__(self, name, lastname, patronymic, login, password, guid=None):
        self.name = name
        self.lastname = lastname
        self.patronymic = patronymic
        self.login = login
        self.password = password
        self.guid = guid

    def __repr__(self):
       return u"<User({}, {}, {}, {})>".format(self.name, self.login, self.password, self.guid)

class LoggedUsers(object):
    def __init__(self, id):
        self.user=id

mapper(Action, actions_table)
mapper(Group, groups_table)
mapper(GroupActions, groupsActions_table)
mapper(User, users_table)
mapper(LoggedUsers, loggedUsers_table)
