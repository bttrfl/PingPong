from pong.routes import routes
from pong.handlers import start_background_tasks, cleanup_background_tasks
from aiohttp import web
import sys
import yaml
import aiomysql
import argparse


def main():
    parser = argparse.ArgumentParser(description="Pong online app server")
    parser.add_argument('--config')
    options = parser.parse_args()

    with open(options.config, 'r') as yml:
        conf = yaml.load(yml)

    app = init_app(conf)

    try:
        web.run_app(app)
    except Exception as e:
        print(e)
        return 1


async def init_app(conf):
    app = web.Application()

    app.conf = conf
    app.db = await aiomysql.connect(**app.conf["mysql"])

    app.add_routes(routes)
    app.add_static("/static", app.conf["static_path"])

    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

    return app


if __name__ == "__main__":
    sys.exit(main())
