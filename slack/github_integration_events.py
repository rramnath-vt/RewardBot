def construct_github_events(app):

    @app.event("message")
    def handle_message_events(body, logger):
        logger.info(body)

    return app
