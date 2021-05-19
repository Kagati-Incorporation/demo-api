import json
import xml.etree.ElementTree as ET
import requests
from django.conf import settings

from .utils import generate_fonepay_hash
from payments.models import (
    IMEPay,
    KhaltiPayment,
    FonepayPayment,
    EsewaPayment,
)
from payments import status

def verify_fonepay(user, data, amount):
    return 200


def verify_khalti(user, token, amount):
    return 200


def verify_esewa(user, data, amount):
    return 200


def verify_imepay(user, data, amount):
    return 200