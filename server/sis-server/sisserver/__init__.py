from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)


    config.add_route('login', '/login')
    config.add_route('home', '/')
    config.add_route('albums', '/albums')
    config.add_route('album', '/album')
    config.add_route('pictures', '/pictures')

    config.add_route('authenticate.json', 'authenticate.json')
    config.add_route('register_worker.json', 'register_worker.json')
    config.add_route('register_picture.json', 'register_picture.json')
    config.add_route('get_albums.json', 'get_albums.json')
    config.add_route('get_picture.jpg', 'get_picture.jpg')
    config.add_route('get_preview.jpg', 'get_preview.jpg')

    config.scan()
    return config.make_wsgi_app()
