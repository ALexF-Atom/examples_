from fastapi import status

invalid_user = {'status_code': status.HTTP_401_UNAUTHORIZED,
                'detail': "Could not validate user"}
                
invalid_user_hobby = {'status_code': status.HTTP_404_NOT_FOUND,
                      'detail': "Could not validate user_hobby_id"}

invalid_token = {'status_code': status.HTTP_401_UNAUTHORIZED,
                 'detail': "Could not validate credentials",
                 'headers': {"WWW-Authenticate": "Bearer"}}

invalid_admin = {'status_code': status.HTTP_401_UNAUTHORIZED,
                 'detail': "Could not validate key"}

invalid_data = {'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'detail': ''}

not_found = {'status_code': status.HTTP_303_SEE_OTHER,
            'detail': "Not found"}

not_found_time = {'status_code': status.HTTP_303_SEE_OTHER,
             'detail': "Not hobbies to day"}
