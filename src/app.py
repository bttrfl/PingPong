from pong.routes import routes
from pong.handlers import start_background_tasks, cleanup_background_tasks
from aiohttp import web
import sys


def main():
    app = web.Application()
    app.add_routes(routes)
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    web.run_app(app)


if __name__ == "__main__":
    sys.exit(main())
