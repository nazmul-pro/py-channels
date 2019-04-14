from django.http import HttpResponse
import jwt, json
from testapp.models import AppUser, AppUserInfo, AppUserToken
def users(request):
    users_json = """
        [
            {
                "name": "Sumon",
                "email": "Sumon@email.com",
                "phone": "555",
                "password": "sumon123"
            },
            {
                "name": "shadhin",
                "email": "shadhin@email.com",
                "phone": "555",
                "password": "sumon123"
            },
            {
                "name": "hussain",
                "email": "hussain@email.com",
                "phone": "555",
                "password": "sumon123"
            }
        ]
    """
    users_py = json.loads(users_json)
    for u in users_py:
        user = AppUser(name=u['name'], email=u['email'], phone=u['phone'], password=u['password'])
        # print(user.id)
        user.save()
        info = AppUserInfo(app_user=user, permissions="later", avatar="later")
        info.save()
        payload = {
            'app_user': user.id,
            'name': user.name,
            'email': user.email
        }
        jwt_token = jwt.encode(payload, "SECRET_KEY").decode('utf-8')
        print(len(jwt_token))
        user_token = AppUserToken(app_user=user, jwt=jwt_token)
        user_token.save()

    return HttpResponse('done')
