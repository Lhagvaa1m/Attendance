"""Handlers package initialization.

This module only exposes the ``bot`` and ``dp`` instances from the
top-level :mod:`mybot` package to keep backward compatibility.  The
actual creation of the bot, dispatcher and storage now lives in
``mybot.__init__`` so that there is a single source of truth.
"""

from mybot import bot, dp

__all__ = ["bot", "dp"]
