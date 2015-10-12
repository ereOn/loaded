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

from .server import server
from .client import Client


def run_io_loop():
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
            "Received Ctrl+C: shutting down I/O loop...",
            fg='yellow',
            bold=True,
        )
    finally:
        IOLoop.current().stop()


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

    server.listen(port=port, address=address)

    click.echo(
        "Started web server on {address}:{port}. Use Ctrl+C to stop.".format(
            address=address,
            port=port,
        ),
    )
    run_io_loop()
    click.echo("Web server stopped.")


@main_loaded.command(help="Run a build on a remote agent.")
@click.option('--port', type=int, default=9995, help="The port to connect to.")
@click.option(
    '--host',
    type=six.text_type,
    default='localhost',
    help="The host to connect to.",
)
@click.pass_context
def build(ctx, port, host):
    if not ctx.obj['DEBUG']:
        logging.getLogger('tornado.access').setLevel(logging.ERROR)

    client = Client(host=host, port=port)
    client.on_complete = IOLoop.current().stop
    client.build()

    run_io_loop()
