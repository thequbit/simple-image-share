import os
import sys

import hashlib

import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Base,
    UserType,
    User,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    
    #with transaction.manager:
    #    model = MyModel(name='one', value=1)
    #    DBSession.add(model)

    system_user_type = UserType.get_user_type_by_name(DBSession, 'system user')
    if system_user_type == None:
        system_user_type = UserType.add_user_type(
            session = DBSession,
            name = 'system user',
            description = 'system user',
        )

    if UserType.get_user_type_by_name(DBSession, 'admin') == None:
        UserType.add_user_type(
            session = DBSession,
            name = 'admin',
            description = 'admin user',
        )

    if UserType.get_user_type_by_name(DBSession, 'user') == None:
        UserType.add_user_type(
            session = DBSession,
            name = 'user',
            description = 'user',
        )

    worker_user_type = UserType.get_user_type_by_name(DBSession, 'worker')
    if worker_user_type == None:
        worker_user_type = UserType.add_user_type(
            session = DBSession,
            name = 'worker',
            description = 'picture gathering worker',
        )

    if User.get_user_by_email(DBSession, 'system') == None:
        User.add_user(
            session = DBSession,
            user_type_id = system_user_type.id, 
            first = 'system',
            last = 'user',
            email = 'system',
            password = hashlib.sha256('password').hexdigest(),
        )

    if User.get_user_by_email(DBSession, 'worker') == None:
        User.add_user(
            session = DBSession,
            user_type_id = worker_user_type.id,
            first = 'worker',
            last = 'user',
            email = 'worker',
            password = hashlib.sha256('password').hexdigest(),
        )

