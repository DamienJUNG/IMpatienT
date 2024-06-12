from callbacks.layout_callback import LayoutCallback
from callbacks.auth_callback import AuthCallback


def load_callbacks(app, args):

    LayoutCallback(app, args).register_callback()
    AuthCallback(app, args).register_callback()