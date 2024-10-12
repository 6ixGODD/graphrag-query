# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import fastapi
import tabulate

from application import handler, config, router
from application.common import middleware, log, graphrag


def create_app() -> fastapi.FastAPI:
    _config = config.get_config()

    log.init_logger(
        level=_config.log_level,
        out_file=_config.log_out_file,
        err_file=_config.log_err_file,
        rotation=_config.log_rotation,
        retention=_config.log_retention,
    )
    graphrag.init_client(_config.graphrag_config_file)

    app = fastapi.FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    handler.init_handler(app)
    middleware.init_middleware(app, api_keys=_config.api_keys)
    router.init_router(app, prefix=_config.app_route_prefix)

    print(tabulate.tabulate(_config.dict().items(), headers=["Configurations", "Values"], tablefmt="fancy_grid"))

    return app
