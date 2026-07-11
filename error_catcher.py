def check_api_none(api_key):
    if not api_key or api_key is None or len(api_key.strip()) == 0:
        raise RuntimeError("api key was not found")


def check_usage_response_none(usage):
    if not usage or usage is None:
        raise RuntimeError("usage response was not found")
