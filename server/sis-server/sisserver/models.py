
import uuid
import datetime
import hashlib

import transaction

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
)

from sqlalchemy import func, desc, asc

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(
        extension=ZopeTransactionExtension(),
        expire_on_commit=False
    )
)
Base = declarative_base()

#class MyModel(Base):
#    __tablename__ = 'models'
#    id = Column(Integer, primary_key=True)
#    name = Column(Text)
#    value = Column(Integer)
#
#Index('my_index', MyModel.name, unique=True, mysql_length=255)

class UserType(Base):

    __tablename__ = 'usertypes'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)

    @classmethod
    def add_user_type(cls, session, name, description):
        with transaction.manager:
            user_type = UserType(
                name = name,
                description = description,
            )
            session.add(user_type)
            transaction.commit()
        return user_type

    @classmethod
    def get_user_type_by_id(cls, session, id):
        with transaction.manager:
            user_type = session.query(
                UserType.name,
                UserType.description,
            ).filter(
                UserType.id == id,
            ).first()
        return user_type

    @classmethod
    def get_user_type_by_name(cls, session, name):
        with transaction.manager:
            user_type = session.query(
                UserType.name,
                UserType.description,
            ).filter(
                UserType.name == name,
            ).first()
        return user_type

    @classmethod
    def get_user_type_from_user_id(cls, session, user_id):
        with transaction.manager:
            user_type = session.query(
                UserType,
            ).join(
                User, User.user_type_id == \
                    UserType.id,
            ).filter(
                User.id == user_id,
            ).first()
        return user_type

    @classmethod
    def get_all_user_types(cls, session):
        with transaction.manager:
            user_types = session.query(
                UserType.name,
                UserType.description,
            ).filter(
            ).all()
        return user_types

class User(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_type_id = Column(Integer, ForeignKey('usertypes.id'))
    first = Column(Text)
    last = Column(Text)
    email = Column(Text)
    pass_salt = Column(Text)
    pass_hash = Column(Text)
    
    @classmethod
    def add_user(cls, session, user_type_id, first, last, email, password):
        with transaction.manager:
            pass_salt = hashlib.sha256(str(uuid.uuid4())).hexdigest()
            pass_hash = hashlib.sha256('{0}{1}'.format(
                password,
                pass_salt,
            )).hexdigest()
            user = User(
                user_type_id = user_type_id,
                first = first,
                last = last,
                email = email,
                pass_salt = pass_salt,
                pass_hash = pass_hash
            )
            session.add(user)
            transaction.commit()
        return user

    @classmethod
    def authenticate_user(cls, session, email, password):
        with transaction.manager:
            user = None
            _user = session.query(
                Users,
            ).filter(
                Users.email == email,
            ).first()
            if _user != None:
                pass_hash = hashlib.sha256('{0}{1}'.format(
                    password,
                    _user.pass_salt,
                )).hexdigest()
                if _user.pass_hash == pass_hash:
                    user = _user
        return user

    @classmethod
    def get_user_by_id(cls, session, id):
        with transaction.manager:
            user = sessin.query(
                User.id,
                User.user_type_id,
                User.first,
                User.last,
                User.email,
            ).filter(
                User.id == id,
            ).first()
        return user

    @classmethod
    def get_user_by_email(cls, session, email):
        with transaction.manager:
            user = session.query(
                User.id,
                User.user_type_id,
                User.first,
                User.last,
                User.email,
            ).filter(
                User.id == email,
            ).first()
        return user

    @classmethod
    def get_all_users(cls, session):
        with transaction.manager:
            users = sessin.query(
                User.id,
                User.user_type_id,
                User.first,
                User.last,
                User.email,
            ).filter(
            ).all()
        return users

class LoginToken(Base):

    __tablename__ = 'logintoken'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(Text, nullable=True)
    token_expire_datetime = Column(DateTime)
    login_datetime = Column(DateTime)

    @classmethod
    def do_login(cls, session, email, password):
        with transaction.manager:
            user = Users.authenticate_user(
                session = session,
                email = email,
                password = password,
            )
            if user != None:
                login_token = cls(
                    user_id = user.id,
                    token = str(uuid.uuid4()),
                    token_expire_datetime = datetime.datetime.now() + \
                        datetime.timedelta(hours=24*30), # expire in 30 days
                    login_datetime = datetime.datetime.now(),
                )
                session.add(login_token)
                transaction.commit() 
        return user, login_token.token

    @classmethod
    def check_authentication(cls, session, token):
        with transaction.manager:
            user = None
            login_token = session.query(
                LoginTokens,
            ).filter(
                LoginTokens.token == token,
                LoginTokens.token_expire_datetime > datetime.datetime.now(),
            ).first()
            if login_token != None:
                user = Users.get_by_id(
                    session = session,
                    user_id = login_token.user_id,
                )
        return user

    @classmethod
    def logout(cls, session, token):
        with transaction.manager:
            login_token = session.query(
                LoginTokens,
            ).filter(
                LoginTokens.token == token,
            ).first()
            session.delete(login_token)
            transaction.commit()
        return

class Worker(Base):

    __tablename__ = 'workers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    registeration_datetime = Column(DateTime)

    @classmethod
    def register_worker(cls, session, user_id):
        with transaction.manager:
            worker = Worker(
                user_id = user_id,
                registration_datetime = datetime.datetime.now(),
            )
            session.add(worker)
            transaction.commit()
        return worker

    @classmethod
    def get_worker_from_user_id(cls, session, user_id):
        with transaction.manager:
            worker = session.query(
                Worker,
            ).filter(
                Worker.user_id == user_id,
            ).first()
        return worker

    @classmethod
    def get_all_workers(cls, session):
        with transaction.manager:
            workers = session.query(
                Worker.id,
                Worker.user_id,
                Worker.registration_datetime,
            ).filter(
            ).all()
        return workers

class Picture(Base):

    __tablename__ = 'pictures'
    id = Column(Integer, primary_key=True)
    filename = Column(Text)
    unique = Column(Text)
    upload_datetime = Column(DateTime)
    
    @classmethod
    def add_picture(cls, session):
        with transaction.manager:
            picture = Picture(
                filename = filename,
                unique = str(uuid.uuid4()),
                upload_datetime = datetime.datetime.now(),
            )
            session.add(picture)
            transaction.commit()
        return picture

    @classmethod
    def get_picture_by_id(cls, session, id):
        with transaction.manager:
            picture = session.query(
                Picture.filename,
                Picture.unique,
                Picture.upload_datetime,
            ).filter(
                Picture.id == id,
            ).first()
        return picture

    @classmethod
    def get_picture_by_filename(cls, session, filename):
        with transaction.manager:
            picture = session.query(
                Picture.filename,
                Picture.unique,
                Picture.upload_datetime,
            ).filter(
                Picture.filename == filename,
            ).first()
        return picture

    @classmethod
    def get_all_pictures(cls, session):
        picture = session.query(
                Picture.filename,
                Picture.unique,
                Picture.upload_datetime,
            ).filter(
                Picture.filename == filename,
            ).first()

class Album(Base):

    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    creator_id = Column(Integer)
    creation_datetime = Column(DateTime)
    display_picture_id = Column(Integer, ForeignKey('pictures.id'), 
        nullable=True,
    )

    @classmethod
    def create_album(cls, session, name, creator_id, creation_datetime, \
            display_picture_id):
        with transaction.manager:
            album = Album(
                name = name,
                creator_id = creator_id,
                creation_datetime = datetime.datetime.now(),
                display_picture_id = display_picture_id,
            )
            session.add(album)
            transaction.commit()
        return album

    @classmethod
    def get_album_by_id(cls, session, id):
        with transaction.manager:
            album = session.query(
                Album.id,
                Album.name,
                Album.creator_id,
                Album.creation_datetime,
                Album.display_picture_id,
            ).filter(
                Album.id == id,
            ).first()
        return album

    @classmethod
    def get_all_albums(cls, session):
        with transaction.manager:
            albums = session.query(
                Album.id,
                Album.name,
                Album.creator_id,
                Album.creation_datetime,
                Album.display_picture_id,
            ).filter(
            ).all()
        return albums

    @classmethod
    def get_all_assigned_albums(cls, session, user_id):
        with transaction.manager:
            albums = session.query(
                Album.id,
                Album.name,
                Album.creator_id,
                Album.creation_datetime,
                Album.display_picture_id,
            ).join(
                 AlbumUserAssignment, AlbumUserAssignment.album_id == \
                     Album.id,
            ).filter(
                AlbumUserAssignment.user_id == user_id,
            ).all()
        return albums

    @classmethod
    def get_album_pictures(cls, session, album_id):
        with transaction.manager:
            pictures = session.query(
                Picture,
            ).join(
                AlbumPictureAssignment.picture_id == \
                    Picture.id
            ).filter(
                AlbumPictureAssignment.album_id == \
                    album_id,
            ).all()
        return pictures

class AlbumPictureAssignment(Base):

    __tablename__ = 'albumpictureassignments'
    id = Column(Integer, primary_key=True)
    picture_id = Column(Integer, ForeignKey('pictures.id'))
    album_id = Column(Integer, ForeignKey('albums.id'))
    assignment_user_id = Column(Integer, ForeignKey('users.id'))
    assignment_datetime = Column(DateTime)
    
    @classmethod
    def set_assignment(cls, session, picture_id, album_id, \
            assignment_user_id):
        with transaction.manager:
            assignment = AlbumPictureAssignment(
                picture_id = picture_id,
                album_id = album_id,
                assignment_user_id = assignment_user_id,
                assignment_datetime = datetime.datetime.now(),
            )
            session.add(assignment)
            transaction.commit()
        return assignment

    @classmethod
    def remove_assignment_by_id(cls, session, id):
        with transaction.manager:
            assignment = session.query(
                Assignment,
            ).filter(
                Assignment.id == id,
            ).first()
            session.delete(assignment)
            transaction.manager()

class AlbumUserAssignment(Base):

    __tablename__ = 'albumuserassignments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    album_id = Column(Integer, ForeignKey('albums.id'))
    assignment_datetime = Column(DateTime)

    @classmethod
    def assign_user_to_album(cls, session, user_id, album_id):
        with transaction.manager:
            assignment = AlbumUserAssignment(
                user_id = user_id,
                album_id = album_id,
                assignment_datetime = datetime.datetime.now(),
            )
            session.add(assignment)
            transaction.commit()
        return assignment

    @classmethod
    def remove_assignment(cls, session, user_id, album_id):
        with transaction.manager:
            assignment = session.query(
                AlbumUserAssignment,
            ).filter(
                AlbumUserAssignment.user_id == user_id,
                AlbumUserAssignment.album_id == album_id,
            ).first()
            session.delete(assignment)
            transaction.commit()


