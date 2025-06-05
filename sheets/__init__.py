"""Sheets package initialization.

Exports ``bot`` and ``dp`` from :mod:`mybot` so that any legacy code
importing them from here continues to work.  Creation of these objects
is centralized in ``mybot.__init__``.
"""

from mybot import bot, dp

__all__ = ["bot", "dp"]
