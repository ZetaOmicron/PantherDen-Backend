from app import access_origin_domains


def set_access_origin(req, resp, resource):
    orig = req.get_header("ORIGIN")
    if orig in access_origin_domains:
        resp.set_header("Access-Control-Allow-Origin", orig)


# TODO: Implement this
def auth(req, resp, resource):
    pass