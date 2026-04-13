import duckdb as ddb

from .clean import QryClean
from .constraints import QryConstraints
from .enums import QryEnums
from .info import QryInfo
from .transform_log import QryTransformLog
from .update import QryUpdate

class QryFltk:
    def __init__(self, conn: ddb.DuckDBPyConnection, table_nm: str):
        self._conn = conn
        self._table_nm = table_nm
        
    def clean(self)->QryClean:
        return QryClean(self._conn, self._table_nm)
    
    def constraints(self)->QryConstraints:
        return QryConstraints(self._conn, self._table_nm)
    
    def enums(self) -> QryEnums:
        return QryEnums(self._conn, self._table_nm)
    
    def into(self) -> QryInfo:
        return QryInfo(self._conn, self._table_nm)
    
    def transform_log(self)->QryTransformLog:
        return QryTransformLog(self._conn, table_nm=self._table_nm)
    
    def update(self)->QryUpdate:
        return QryUpdate(self._conn, table_nm=self._table_nm)
    
    
        
    