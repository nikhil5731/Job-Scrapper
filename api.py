from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from internshala import extractAllJobsInternshalaAPI
from unstop import extractAllJobsUnstopAPI
from naukri import extractAllJobsNaukriAPI
from cuvette import extractAllCuvetteAPI
from linkedin import extractAllJobsLinkedInAPI


app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def index():
    return {"message": "Jobs Scrapper!"}


@socketio.on("message")
def message(message):
    print("Received message: " + str(message))
    emit("response", message)


@socketio.on("scrapeInternhsala")
def scrapeInternhsala(msg):
    try:
        extractAllJobsInternshalaAPI(msg["url"], msg["jobType"], msg["currPage"])
    except KeyError as e:
        print(f"KeyError: {e} - The session may be disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")


@socketio.on("scrapeUnstop")
def scrapeUnstop(msg):
    try:
        extractAllJobsUnstopAPI(msg["url"], msg["currPage"])
    except KeyError as e:
        print(f"KeyError: {e} - The session may be disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")


@socketio.on("scrapeNaukri")
def scrapeNaukri(msg):
    try:
        extractAllJobsNaukriAPI(msg["url"], msg["currPage"])
    except KeyError as e:
        print(f"KeyError: {e} - The session may be disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")


@socketio.on("scrapeCuvette")
def scrapeCuvette(msg):
    try:
        extractAllCuvetteAPI(msg["url"], msg["currPage"])
    except KeyError as e:
        print(f"KeyError: {e} - The session may be disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")


@socketio.on("scrapeLinkedin")
def scrapeLinkedin(msg):
    try:
        extractAllJobsLinkedInAPI(msg["url"], msg["currPage"])
    except KeyError as e:
        print(f"KeyError: {e} - The session may be disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    socketio.run(app)
