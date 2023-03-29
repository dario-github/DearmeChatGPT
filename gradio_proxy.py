from flask import Flask, request, jsonify
from flask_cors import CORS
import gradio as gr

app = Flask(__name__)
CORS(app)


def forward_request(*args, **kwargs):
    response = demo.interface.process(request.get_json())
    return jsonify(response)


app.add_url_rule('/chat', view_func=forward_request, methods=["POST"])

if __name__ == "__main__":
    reload_javascript()
    # if running in Docker
    if dockerflag:
        if authflag:
            app.run(host="0.0.0.0", port=7860)
        else:
            app.run(host="0.0.0.0", port=7860)
    # if not running in Docker
    else:
        if authflag:
            app.run(host="0.0.0.0", port=7860)
        else:
            app.run(host="0.0.0.0", port=7860)
