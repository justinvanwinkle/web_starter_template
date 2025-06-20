from werkzeug.wrappers import Response

from webapp.lib.render import renderer


def homepage(req):
    return Response(renderer.render("html/landing.html"), mimetype="text/html")
