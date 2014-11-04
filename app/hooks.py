from app import access_origin_domains


def set_access_origin(req, resp, resource):
    host = req.host
    if host in access_origin_domains:
        resp.set_header("Access-Control-Allow-Origin", host)


# TODO: Implement this
def auth(req, resp, resource):
    pass