from ._qry_repo import QryRepo
from .clean import QryClean
from .constraints import QryConstraints
from .enums import QryEnums
from .info import QryInfo
from .transform_log import QryTransformLog
from .update import QryUpdate


class QryFltk(QryRepo):
    @property
    def clean(self) -> QryRepo:
        return QryClean(self._conn, self._table_nm)

    @property
    def constraints(self) -> QryRepo:
        return QryConstraints(self._conn, self._table_nm)

    @property
    def enums(self) -> QryRepo:
        return QryEnums(self._conn, self._table_nm)

    @property
    def info(self) -> QryRepo:
        return QryInfo(self._conn, self._table_nm)

    @property
    def transform_log(self) -> QryRepo:
        return QryTransformLog(self._conn, table_nm=self._table_nm)

    @property
    def update(self) -> QryRepo:
        return QryUpdate(self._conn, table_nm=self._table_nm)
