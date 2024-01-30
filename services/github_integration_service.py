import os
from datetime import datetime
import requests
import mysql
from dotenv import load_dotenv

load_dotenv()


def is_pull_request_merged(body):
    if body["action"] == "closed" and body["pull_request"]["merged"]:
        return True
    return False


def store_points(body, mysql_connection):
    mycursor = mysql_connection.cursor()
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d')
    user = body["pull_request"]["user"]["login"]

    try:

        if mysql_connection.in_transaction:
            mysql_connection.rollback()
            print("Rolling back previous transaction...")

        mysql_connection.start_transaction()

        sql = "SELECT * FROM employee WHERE github_id = %s"
        val = (user, )
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        awardee = result[0][2]

        sql1 = "UPDATE employee SET points = points + %s WHERE slack_id = %s"
        val1 = (10, awardee)
        mycursor.execute(sql1, val1)

        sql2 = "INSERT INTO audit (awarder, awardee, award, award_date) VALUES (%s, %s, %s, %s)"
        val2 = ("github", awardee,
                "GitHub", formatted_date)
        mycursor.execute(sql2, val2)

        mysql_connection.commit()

    except mysql.connector.Error as error:
        print(error)
        print("Error occurred during transaction. Rolling back changes.")
        mysql_connection.rollback()

    finally:
        mycursor.close()


def send_github_slack_message(body):
    user = body["pull_request"]["user"]["login"]
    url = body["pull_request"]["html_url"]

    body = {
        "blocks": [
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "GitHub Award 💻",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"{user} gets an award for GitHub contribution!",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"Here is the PR, {url}!",
                    "emoji": True
                }
            }
        ]
    }

    requests.post(
        os.environ.get("SLACK_WEBHOOK_URL"),
        json=body,
        timeout=5
    )
