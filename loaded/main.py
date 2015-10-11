"""
Scripts.
"""

import click
import logging
import platform
import six

from tornado.ioloop import (
    IOLoop,
    PeriodicCallback,
)

from .server import agent_application


@click.group()
@click.option('-d', '--debug/--no-debug', default=False)
@click.pass_context
def main_loaded(ctx, debug):
    """
    Loaded build agent.
    """
    ctx.obj = {}

    if debug:
        click.secho("Running in debug mode.", fg='cyan')

    ctx.obj['DEBUG'] = debug

    logging.basicConfig()

@main_loaded.command(help="Run a Loaded agent locally.")
@click.option('--port', type=int, default=9995, help="The port to listen on.")
@click.option(
    '--address',
    type=six.text_type,
    default='0.0.0.0',
    help="The address to listen on.",
)
@click.pass_context
def agent(ctx, port, address):
    if not ctx.obj['DEBUG']:
        logging.getLogger('tornado.access').setLevel(logging.ERROR)

    agent_application.listen(port=port, address=address)
    click.echo(agent_application.default_host)

    click.echo(
        "Started web server on {address}:{port}".format(
            address=address,
            port=port,
        ),
    )

    if platform.system() == 'Windows':
        # On Windows, select call can't be interrupted by SIGINT so we add
        # a periodic callback that will wake-up the event loop and raise
        # the KeyboardInterrupt if needed.
        periodic_callback = PeriodicCallback(lambda: None, 100)
        periodic_callback.start()

    try:
        IOLoop.current().start()
    except KeyboardInterrupt as ex:
        click.secho(
            "Received Ctrl+C: shutting down web server...",
            fg='yellow',
            bold=True,
        )
    finally:
        IOLoop.current().stop()
        click.echo("Web server stopped.")
