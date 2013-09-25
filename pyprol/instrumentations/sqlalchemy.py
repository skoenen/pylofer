import importlib

from pyprol.measurement import measurement
from logging import getLogger


log = getLogger('pyprol.instrumentations.sqlalchemy')

def inject_into_session_commit(config):
    _sqlalchemy_session = importlib.import_module('sqlalchemy.orm.session')
    _sqlalchemy_session_class = _sqlalchemy_session.Session
    _sqlalchemy_session_class_commit = _sqlalchemy_session_class.commit

    def commit(self):
        measure = measurement.enable("sqlalchemy.orm.session.Session.commit")
        result = _sqlalchemy_session_class_commit(self)
        measurement.disable(measure)
        return result

    _sqlalchemy_session_class.commit = commit

def inject(config):
    try:
        inject_into_session_commit(config)

    except ImportError, e:
        log.info("No `sqlalchemy.orm.session` in current python context.")
        log.debug(e)

