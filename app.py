import os
import signal
import atexit
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import load_dotenv
from slack.award_points_events import construct_award_points_events
from slack.github_integration_events import construct_github_events
from slack.leaderboard_events import construct_leaderboard_events
from services import github_integration_service
from settings import mysql_settings


mysql_settings.init()
mysql_connection = mysql_settings.connection

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

app = construct_award_points_events(app, mysql_connection)
app = construct_github_events(app)
app = construct_leaderboard_events(app, mysql_connection)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/hook/github", methods=["POST"])
def handle_github_hook():
    body = request.json
    if github_integration_service.is_pull_request_merged(body):
        github_integration_service.store_points(body, mysql_connection)
        github_integration_service.send_github_slack_message(body)

    return "200"


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@flask_app.route("/slack/command", methods=["POST"])
def slack_command():
    return handler.handle(request)


@flask_app.route("/slack/interactive-endpoint", methods=["POST"])
def slack_interactive():
    return handler.handle(request)


def handle_exit():
    mysql_connection.close()


atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

if __name__ == "__main__":
    flask_app.run(port=4001)
