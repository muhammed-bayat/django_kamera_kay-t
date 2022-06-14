import requests
from datetime import datetime
from apps.common.sms_sender.sms_enum import SmsHeadersEnum


class SMSRequest:
    def __init__(self, username, password):
        self.username: str = username
        self.password: str = password
        self.req_address = f"http://panel.1sms.com.tr:8080/api/campaignidlist/v1?username={self.username}&password={self.password}&page=0"
        self.headers = {"Content-Type": "application/xml"}

    def get_sent_message_list(self):
        r = requests.get(self.req_address, headers=self.headers)
        print(r)

    def send_sms(self, numbers: list, message_header=SmsHeadersEnum.blmturkiye.value, message_body="", validity="2880"):
        """
        1-N: same message for N number
        """
        number_text = SMSRequest._get_number_string(numbers)
        url = "http://panel.1sms.com.tr:8080/api/smspost/v1"
        m_body = f"""
        <sms>
            <username>{self.username}</username>
            <password>{self.password}</password>
            <header>{message_header}</header>
            <validity>{validity}</validity>
            <sendDateTime>{datetime.now().strftime("%Y.%m.%d.%H.%M.%S")}</sendDateTime>
            <message>
                <gsm>
                    {number_text}
                </gsm>
                <msg><![CDATA[{message_body}]]></msg>
            </message>
        </sms>
        """
        r = requests.post(url, data=m_body.encode('utf-8'), headers=self.headers)
        return r.text

    def check_credit(self):
        url = f"http://panel.1sms.com.tr:8080/api/credit/v1?username={self.username}&password={self.password}"
        r = requests.get(url, headers=self.headers)
        return r.text

    def get_header(self):
        url = f"http://panel.1sms.com.tr:8080/api/originator/v1?username={self.username}&password={self.password}"
        r = requests.get(url, headers=self.headers)
        return r.text

    @staticmethod
    def _get_number_string(numbers):
        t = ""
        number_list = SMSRequest._phonenumber_corrector(numbers)
        for number in number_list:
            t = t + f"<no> {number} </no>\n"
        return t

    @staticmethod
    def _phonenumber_corrector(numbers):
        new_number_list = []
        for number in numbers:
            index = number.index("5")
            number = number.replace(" ","")
            number = "90" + number[index:]
            if len(number) == 12 and number.isdecimal():
                new_number_list.append(number)
        return new_number_list
