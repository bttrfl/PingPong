from pong.routes import routes
from pong.handlers import start_background_tasks, cleanup_background_tasks
from aiohttp import web
import sys
import yaml
import aiomysql
import argparse
import jinja2
import aiohttp_jinja2
import aioredis
from aiohttp_session import setup
from aiohttp_session.redis_storage import RedisStorage


#runs pong server
def main():
    parser = argparse.ArgumentParser(description="Pong online app server")
    parser.add_argument('--config')
    options = parser.parse_args()

    with open(options.config, 'r') as yml:
        conf = yaml.load(yml, Loader=yaml.CLoader)

    app = init_app(conf)

    try:
        web.run_app(app)
    except Exception as e:
        print(e)
        return 1


#setup routes, static files etc, connect to db
async def init_app(conf):
    app = web.Application()
    app.conf = conf

    #setup session storage
    redis = await aioredis.create_pool((app.conf["redis_addr"], 6379))
    setup(app, RedisStorage(redis))

    app.db = await aiomysql.connect(**app.conf["mysql"], autocommit=True)

    app.add_routes(routes)
    app.router.add_static("/static", app.conf["static_path"])
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(app.conf["template_path"]))

    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

    return app


if __name__ == "__main__":
    sys.exit(main())
