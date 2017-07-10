import os
import tempfile
import string
import random
from itsdangerous import URLSafeTimedSerializer
from captcha.image import ImageCaptcha

from config import get_config_obj

serializer = URLSafeTimedSerializer(get_config_obj().SECRET_KEY)
FONTS_PATH = os.path.join(get_config_obj().PROJECT_PATH, "static/fonts")
image = ImageCaptcha(fonts=[os.path.join(FONTS_PATH, 'CourierNew-Bold.ttf'),
                            os.path.join(FONTS_PATH, 'LiberationMono-Bold.ttf')])


class Captcha(object):
    def __init__(self, captcha_code=None):
        if captcha_code:
            self.captcha_code = captcha_code
        else:
            self.captcha_code = ''.join(random.sample(string.digits + string.lowercase + string.uppercase, 6))
        self.captcha_id = serializer.dumps(self.captcha_code)

    def image(self):
        data = image.generate(self.captcha_code)
        return data

    def save(self):
        file_path = tempfile.mkstemp(prefix="INFO-SUB-CAPTCHA-", suffix=".png")
        image.write(self.captcha_code, file_path)
        return file_path

    def validate(self, code):
        code = code.strip()
        if self.captcha_code.lower() == code.lower():
            return True
        return False

    @classmethod
    def get_by_captcha_id(cls, captcha_id, max_age=60 * 30):
        try:
            captcha_code = serializer.loads(captcha_id, max_age=max_age)
        except:
            captcha_code = None
        if not captcha_code:
            return None
        return cls(captcha_code)
