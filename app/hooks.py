# TODO: Have a list of allowed domains
def set_access_origin(req, resp, resource):
    resp.set_header("Access-Control-Allow-Origin", "Add domains here")


# TODO: Implement this
def auth(req, resp, resource):
    pass