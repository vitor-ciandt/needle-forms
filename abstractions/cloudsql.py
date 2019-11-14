"""Class for centralizing CloudSql operations"""
import logging
import operator

from typing import List
from pydal import DAL, Field
from pydal.objects import Table, Query


__all__ = ("CloudSql",)


_LOG_PREFIX_ = "[CLOUDSQL]%s"


class CloudSql:
    """
    Class for abstracting the access of the Mysql or Postgresql on
    CloudSQL
    """

    db: DAL = None

    def __init__(self, uri: str, table_name: str, columns: list):
        """Constructor"""
        self.db = DAL(uri, migrate=False)
        self.table = self.get_table_instance(table_name, columns)

    @staticmethod
    def get_fields(columns: list) -> List[Field]:
        """Get list of pydal field objects"""
        return [Field(i) for i in columns]

    def get_table_instance(self, table_name: str, columns: list) -> Table:
        """Get table of pydal"""
        columns = self.get_fields(columns)
        if table_name not in self.db.tables:
            self.db.define_table(table_name, *columns)
        return self.db[table_name]

    def get_query(self, column: str, value: str,
                  str_operator: str = "=") -> Query:
        """Get a pydal query object"""
        ops = {'>': operator.gt,
               '<': operator.lt,
               '>=': operator.ge,
               '<=': operator.le,
               '=': operator.eq,
               '!=': operator.ne}
        column = getattr(self.table, column)
        return ops[str_operator](column, value)

    def filter(self, filters: List[dict]) -> (List[dict], List):
        """
        Filter item from table
        The param format is:
            [{'column': 'id', 'value': 1, 'str_operator': '!='}]
        """
        query = []
        for idx, filter_item in enumerate(filters):
            query_obj = self.get_query(**filter_item)
            if idx == 0:
                query = query_obj
            else:
                query &= query_obj

        if query:
            return self.db(query).select().as_list()
        return []

    def all(self) -> List[dict]:
        """"Return all items from table"""
        items = self.db(self.table).select().as_list()
        return items
