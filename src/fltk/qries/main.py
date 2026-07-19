from .base import QryRepo
from .clean import QryClean
from .constraints import QryConstraints
from .enums import QryEnums
from .info import QryInfo
from .transform_log import QryTransformLog
from .update import QryUpdate


class QryFltk(QryRepo):
    @property
    def clean(self) -> QryRepo:
        return QryClean(self.conn, table_nm=self.table_nm)

    @property
    def constraints(self) -> QryRepo:
        return QryConstraints(self.conn, table_nm=self.table_nm)

    @property
    def enums(self) -> QryRepo:
        return QryEnums(self.conn, table_nm=self.table_nm)

    @property
    def info(self) -> QryRepo:
        return QryInfo(self.conn, table_nm=self.table_nm)

    @property
    def transform_log(self) -> QryRepo:
        return QryTransformLog(self.conn, table_nm=self.table_nm)

    @property
    def update(self) -> QryRepo:
        return QryUpdate(self.conn, table_nm=self.table_nm)
