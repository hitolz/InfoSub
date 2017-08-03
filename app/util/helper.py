def str2bool(v, default=False):
    if str(v).lower() in ("yes", "true", "t", "1"):
        return True
    return default


