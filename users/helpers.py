import firebase_admin
from django.conf import settings
from firebase_admin import credentials
from firebase_admin.auth import verify_id_token

from .models import User


def validate_id_token(id_token):
    cred = credentials.Certificate(str(settings.FIREBASE_KEY_PATH))
    default_app = firebase_admin.initialize_app(cred)

    decoded = verify_id_token(id_token)
    uuid = decoded.get('uid')
    email = decoded.get('email')
    try:
        profile_pic = decoded.get('photoURL')
    except:
        profile_pic = None
    phone_number = decoded.get('phoneNumber')
    if uuid and email:
        user, created = User.objects.get_or_create(email=email)
        if created:
            # need to save other fields too
            user.firebase_uuid = uuid
            if profile_pic:
                user.profile_pic = profile_pic
            user.phone_number = phone_number
            user.save()
    else:
        user = None
    return user
