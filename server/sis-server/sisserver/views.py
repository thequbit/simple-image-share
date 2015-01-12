from pyramid.response import Response
from pyramid.view import view_config
from pyramid.response import FileResponse

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    UserType,
    User,
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

def auth(request):
    
    success = False
    token = None
    user = None
    try:
        token = request.GET['token']
        user, token = LoginToken.check_authentication(token)
        if user != None and token != None:
            success = True
    except:
        pass
    
    return success, token, user

@view_config(route_name='authenticate.json')
def web_authenticate(request):

    result = {'success': False}
    try:
            
        success = False
        token = None
        user = None
        try:
            email = request.GET['email']
            password = request.GET['password']
        except:
            raise Exception("Missing Fields")
        
        user, token = LoginToken.do_login(email, password)
        if user != None and token != None:
            success = True

        result['token'] = token
        result['success'] = success

    except:
        pass

    make_response(result)

@view_config(route_name='register_worker.json')
def web_register_worker(request):

    result = {'success': False}
    try:

        success, token, user = auth(request)

        if success == False:
            raise Exception('Invalid Creds')

        user_type = UserType.get_user_type_from_user_id(
            session = DBSession,
            user_id = user.id,
        )

        if user_type != 'worker':
           raise Exception('Incorrect Creds')

        worker = Worker.get_worker_from_user_id(
            session = DBSession,
            user_id = user_id,
        )

        if worker == None:
            worker = Worker.register_worker(
                session = DBSession,
                user_id = user_id,
            )

        result['worker_id'] = worker.id
        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    make_response(result)

@view_config(route_name='get_albums.json')
def web_get_albums(request):

    result = {'success': False}
    try:

        success, token, user = auth(request)

        if success == False:
            raise Exception('Invalid Creds')

        _albums = Album.get_all_assigned_albums(
            session = DBSession,
            user_id = user.id,
        )

        albums = []
        for album_id, album_name, album_creator_id, album_creation_datetime, \
                album_display_picture_id in _albums:
            albums.append({
                'id': album_id,
                'name': album_name,
                'creator_id': album_creator_id,
                'creation_datetime': str(album_creation_datetime),
                'display_picture_id': display_picture_id,
            })

        result['albums'] = albums

        result['success'] = True

    except Exception, e:
        result['error_text'] = str(e)

    make_response(result)

@view_config(route_name='get_picture.jpg')
def web_get_picture(request):

    result = {'success': False}
    try:

        success, token, user = auth(request)

        if success == False:
            raise Exception('Invalid Creds')

        try:
            picture_id = request.GET['id']
        except:
            raise Exception('Missing Field')

        picture = Picture.get_picture_by_id(
            session = DBSession,
            id = picture_id,
        )

        response = FileResponse(
            picture.filename,
            request=request,
            content_type='image/jpeg'
        )

    except Exception, e:
        pass

    return response


