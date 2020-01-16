
# Run a test server.
from app import app


@app.route("/", methods=["GET"])
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
