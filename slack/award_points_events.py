from services import award_points_service


def construct_award_points_events(app, mysql_connection):
    @app.command("/reward")
    def handle_reward_command(ack, body, client):
        award_points_service.award_points(ack, client, body)

    @app.action("users_select-action")
    def handle_user_selection(ack, body, logger):
        ack()
        logger.info(body)

    @app.action("static_select-action")
    def handle_static_selection(ack, body, logger):
        ack()
        logger.info(body)

    @app.view("reward_modal")
    def handle_reward_modal_submission(ack, body, view, client):
        award_info = award_points_service.validate_award(
            ack, body, view, mysql_connection)

        if award_info:
            award_points_service.send_award_message(client, award_info)
            award_points_service.store_points(award_info, mysql_connection)

    return app
