import flask
from flask import request
from flask_cors import CORS
from public.app import App
from public.special.pages.layout import Layout
from public.special.pages.not_found import Not_Found
from public.special.pages.error import Error
from public.special.util import compare_dy_url, render

server = flask.Flask(__name__,
                     static_folder="./public/assets",
                     template_folder="./public/views")

CORS(server)

@server.route("/")
def index():
  return render(App(None), Layout)


@server.route("/<var>")
def dynamic(var):
  if compare_dy_url("/"):
    return render(App(var), Layout)
  else:
    return not_found(None)


@server.route("/name")
def vars():
  params = request.args.to_dict()
  if params:
    return render(App(params), Layout)
  else:
    return render(Error("Requires variable", 404), title="Invalid Request", Layout=Layout)


@server.errorhandler(404)
def not_found(err):
  return render(Not_Found(), title="404 ERROR", Layout=Layout), 404


if __name__ == "__main__":
  server.run(host="0.0.0.0", port=8080)