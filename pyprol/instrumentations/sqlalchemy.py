import importlib

from pyprol.measurement import measurement
from logging import getLogger


log = getLogger('pyprol.instrumentations.sqlalchemy')

def inject_into_session_commit(config):
    _session = importlib.import_module('sqlalchemy.orm.session')
    _session_class = _session.Session
    _session_commit = _session_class.commit

    def commit(self):
        measure = measurement.enable("sqlalchemy.orm.session.Session.commit")
        result = _session_commit(self)
        measurement.disable(measure)
        return result

    _session_class.commit = commit

def inject_into_session_transaction_commit(config):
    _session = importlib.import_module('sqlalchemy.orm.session')
    _session_transaction = _session.SessionTransaction
    _transaction_commit = _session_transaction.commit

    def commit(self):
        measure = measurement.enable(
                "sqlalchemy.orm.session.SessionTransaction.commit")
        result = _transaction_commit(self)
        measurement.disable(measure)
        return result

    _session_transaction.commit = commit

def inject_into_session_transaction_close(config):
    _session = importlib.import_module('sqlalchemy.orm.session')
    _session_transaction = _session.SessionTransaction
    _transaction_close = _session_transaction.close

    def close(self):
        measure = measurement.enable(
                "sqlalchemy.orm.session.SessionTransaction.commit")
        result = _transaction_close(self)
        measurement.disable(measure)
        return result

    _session_transaction.close = close

def inject(config):
    try:
        inject_into_session_commit(config)
        inject_into_session_transaction_commit(config)
        inject_into_session_transaction_close(config)

    except ImportError as e:
        log.info("No `sqlalchemy.orm.session` in current python context.")
        log.debug(e)

