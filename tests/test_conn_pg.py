"""Test the postgreSQL connection."""

from sqlalchemy import engine

import fltk.conn.connect_pg as conn


def test_engine_gp():
    out = conn.get_engine()
    assert isinstance(out, engine.base.Engine)
