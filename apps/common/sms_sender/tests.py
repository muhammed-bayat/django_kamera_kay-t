from .sms_sender import SMSRequest
from unittest import TestCase

class SmsTest(TestCase):
    test_list = [
        "35023542354",
        "+05555555555",
        "+9000005023542354",
        "5023542354",
        "5023542354",
        "50235423  54",
        "502  3542354",
        "5023542sdfg354",
        "50235 42354",
        "5023542354",
        "5023542354",
        "50 23542 354",
        "502  35423  54",
        "5023542 3    54",
        "50235 21754",
        "502354254863254",
        "5023542354",
        "5023542354",
        "5023542354",
        "05023542354",
        "905023542354",
    ]

    def test_check_number(self):
        aa = SMSRequest._phonenumber_corrector(self.test_list)
        print(aa)
        return SMSRequest._phonenumber_corrector(self.test_list)


