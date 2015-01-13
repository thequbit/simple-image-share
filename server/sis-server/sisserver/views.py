import os
import json
import datetime
import uuid
import hashlib

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.response import FileResponse

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    UserType,
    User,
    LoginToken,
    Worker,
    Picture,
    Album,
    AlbumPictureAssignment,
    AlbumUserAssignment,
)

def make_response(resp_dict):

    print "[DEBUG]"
    print resp_dict
    print '\n'

    resp = Response(json.dumps(resp_dict), content_type='application/json', charset='utf8')
    resp.headerlist.append(('Access-Control-Allow-Origin', '*'))

    return resp

#def auth(request):
#    
#    success = False
#    token = None
#    user = None
#    try:
#        token = request.GET['token']
#        user, token = LoginToken.check_authentication(token)
#        if user != None and token != None:
#            success = True
#    except:
#        pass
#    
#    return success, token, user

def check_auth(request):

    token = None
    try:
        token = request.cookies['token']
        
        if token == None or token == '':
            raise Exception('invalid token format')
    except Exception, e:
        #print "check_auth() exception: {0}".format(str(e)) 
        #print "\n"
        pass
        
    try:
        token = request.GET['token']
        if token == None or token == '':
            raise Exception('invalid token format')
    except:
        pass
        
    if token == None or token == '':
        raise Exception('Invalid Token')
        
    user = LoginToken.check_authentication(
        session = DBSession,
        token = token,
    )
    
    if user == None:
        raise Exception('Invalid token')
    
    return user, token

@view_config(route_name='login', renderer='templates/login.mak')
def web_login(request):

    return {}

@view_config(route_name='home', renderer='templates/index.mak')
def web_home(request):

    return {}

@view_config(route_name='albums', renderer='templates/albums.mak')
def web_albums(request):

    try:
        user, token = check_auth(request)

        _albums = Albums.get_all_assigned_albums(
            session = DBSession,
            user_id = user.id,
        )

        albums = []
        for id, name, creation_datetime, creator_id, creator_first, creator_last, \
                picture_unique in _albums:
            albums.append({
                'id': id,
                'name': name,
                'creator_first': creator_first,
                'creator_last': creator_last,
                'picture_unique': picture_unique,
            })

    except:
        pass

    return {'user': user, 'albums': albums}

@view_config(route_name='album', renderer='templates/album.mak')
def web_album(request):

    return {}

@view_config(route_name='pictures', renderer='templates/pictures.mak')
def web_pictures(request):

    pictures = Picture.get_all_pictures(
        session = DBSession,
        start = 0,
        count = 12,
    )

    return {'pictures': pictures}

@view_config(route_name='authenticate.json')
def web_authenticate(request):

    result = {'success': False}
    #try:
    if True:

        success = False
        token = None
        user = None
        try:
            email = request.GET['email']
            password = request.GET['password']
        except:
            raise Exception("Missing Fields")
        
        user, token = LoginToken.do_login(
            session = DBSession,
            email = email,
            password = password
        )
        if user != None and token != None:
            success = True

        result['token'] = token
        result['success'] = success

    #except:
    #    pass

    return make_response(result)

@view_config(route_name='register_worker.json')
def web_register_worker(request):

    result = {'success': False}
    try:

        user, token = check_auth(request)

        user_type = UserType.get_user_type_from_user_id(
            session = DBSession,
            user_id = user.id,
        )

        if user_type.name != 'worker':
           raise Exception('Incorrect Creds')

        worker = Worker.get_worker_from_user_id(
            session = DBSession,
            user_id = user.id,
        )

        if worker == None:
            worker = Worker.register_worker(
                session = DBSession,
                user_id = user.id,
            )

        result['worker_id'] = worker.id
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return make_response(result)

@view_config(route_name='register_picture.json')
def web_register_picture(request):

    result = {'success': False}
    try:

        user, token = check_auth(request)

        user_type = UserType.get_user_type_from_user_id(
            session = DBSession,
            user_id = user.id,
        )

        if user_type.name != 'worker':
           raise Exception('Incorrect Creds')

        try:
            file_name = request.POST['file_name']
            folder_name = request.POST['folder_name']
            folder_path = request.POST['folder_path']
        except:
            result['error_text'] = "Missing or invalid field"
            raise Exception("Missing or invalid field")

        picture = Picture.get_picture_by_file_name(
            session = DBSession,
            file_name = file_name,
        )

        if picture == None:
            picture = Picture.add_picture(
                session = DBSession,
                file_name = file_name,
                folder_name = folder_name,
                folder_path = folder_path,
            )

        result['picture_id'] = picture.id

        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return make_response(result)

@view_config(route_name='get_albums.json')
def web_get_albums(request):

    result = {'success': False}
    try:

        user, token = check_auth(request)

        _albums = Album.get_all_assigned_albums(
            session = DBSession,
            user_id = user.id,
        )

        albums = []
        for album_id, album_name, album_creator_id, album_creation_datetime, \
                album_display_picture_unique in _albums:
            albums.append({
                'id': album_id,
                'name': album_name,
                'creator_id': album_creator_id,
                'creation_datetime': str(album_creation_datetime),
                'display_picture_unique': alumb_display_picture_uniqie,
            })

        result['albums'] = albums

        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    return make_response(result)

@view_config(route_name='get_picture.jpg')
def web_get_picture(request):

    result = {'success': False}
    #try:
    if True:

        #user, token = check_auth(request)

        try:
            unique = request.GET['unique']
        except:
            raise Exception('Missing Field')

        picture = Picture.get_picture_by_unique(
            session = DBSession,
            unique = unique,
        )

        response = FileResponse(
            picture.file_name,
            request=request,
            content_type='image/jpeg'
        )

    #except Exception, e:
    #    pass

    return response

@view_config(route_name='get_preview.jpg')
def web_get_preview(request):

    result = {'success': False}
    #try:
    if True:

        #user, token = check_auth(request)

        try:
            unique = request.GET['unique']
        except:
            raise Exception('Missing Field')

        picture = Picture.get_picture_by_unique(
            session = DBSession,
            unique = unique,
        )

        response = FileResponse(
            "{0}_preview.jpg".format(picture.file_name),
            request=request,
            content_type='image/jpeg'
        )

    #except Exception, e:
    #    pass

    return response
