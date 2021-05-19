import hashlib

from django.utils import timezone
from referrals.models import (
    ReferralInfo,
)


def generate_code(email):
    hash_unique = False
    while not hash_unique:
        hash_string = email + str(timezone.now())
        hash_object = hashlib.sha256(hash_string.encode('utf-8'))
        final_hash = hash_object.hexdigest()[:10]
        if not ReferralInfo.objects.filter(code=final_hash).exists():
            hash_unique = True
    return final_hash
