"""Metrics dashboard entry point: wiring only."""

from __future__ import annotations

import logging

from dotenv import load_dotenv
from flask import Flask

from config import Settings
from scoring.store import MetricStore
from web.routes import bp


def create_app(settings: Settings | None = None) -> Flask:
    if settings is None:
        load_dotenv()
        settings = Settings.from_env()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.secret_key
    app.config["PAGE_SIZE"] = settings.page_size
    app.extensions["metric_store"] = MetricStore(
        settings.metrics_path, settings.data_path
    )
    app.register_blueprint(bp)
    return app


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    settings = Settings.from_env()
    create_app(settings).run(
        host=settings.host, port=settings.port, debug=settings.debug
    )
