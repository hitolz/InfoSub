import os
import tempfile
import string
import random
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from captcha.image import ImageCaptcha


serializer = URLSafeTimedSerializer(current_app.config.get("SECRET_KEY"))
FONTS_PATH = os.path.join(current_app.config.get("PROJECT_PATH"), "static/fonts")
image = ImageCaptcha(fonts=[os.path.join(FONTS_PATH, 'CourierNew-Bold.ttf'),
                            os.path.join(FONTS_PATH, 'LiberationMono-Bold.ttf')])


class Captcha(object):

    def __init__(self, captcha_code=None):
        if captcha_code:
            self.captcha_code = captcha_code
        else:
            self.captcha_code = ''.join(random.sample(string.digits + string.lowercase + string.uppercase, 6))
        self.captcha_id = serializer.dumps(captcha_code)

    def image(self):
        data = image.generate(self.captcha_code)
        return data

    def save(self):
        file_path = tempfile.mkstemp(prefix="INFO-SUB-CAPTCHA-", suffix=".png")
        image.write(self.captcha_code, file_path)
        return file_path

    @classmethod
    def get_by_captcha_id(cls, captcha_id):
        captcha_code = serializer.loads(captcha_id)
        return cls(captcha_code)

