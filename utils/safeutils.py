from urllib.parse import urlparse, urljoin

from flask import request


def is_safe_url(target):
    """
    验证url地址是否属于当前域名的url地址
    :param target:
    :return:
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc
