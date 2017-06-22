class BaseError(Exception):

    def __init__(self, error_id, error_msg, error_code):
        self.error_id = error_id
        self.error_msg = error_msg
        self.error_code = error_code

    def __str__(self):
        return "<{ID}> {MSG}, {CODE}".format(
            ID=self.error_id,
            MSG=self.error_msg,
            CODE=self.error_code,
        )


class ConfigError(BaseError):

    def __init__(self, error_msg):
        super(ConfigError, self).__init__("config_error", error_msg, 500)

