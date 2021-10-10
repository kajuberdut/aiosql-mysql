import pymysql


class SyncDriverAdapterProtocol(Protocol):
    def process_sql(self, query_name: str, op_type: SQLOperationType, sql: str) -> str:
        ...

    def select(
        self,
        conn: Any,
        query_name: str,
        sql: str,
        parameters: Union[List, Dict],
        record_class=Optional[Callable],
    ) -> List:
        ...

    def select_one(
        self,
        conn: Any,
        query_name: str,
        sql: str,
        parameters: Union[List, Dict],
        record_class=Optional[Callable],
    ) -> Optional[Any]:
        ...

    def select_cursor(
        self, conn: Any, query_name: str, sql: str, parameters: Union[List, Dict]
    ) -> ContextManager[Any]:
        ...

    def insert_update_delete(
        self, conn: Any, query_name: str, sql: str, parameters: Union[List, Dict]
    ) -> None:
        ...

    def insert_update_delete_many(
        self, conn: Any, query_name: str, sql: str, parameters: Union[List, Dict]
    ) -> None:
        ...

    def insert_returning(
        self, conn: Any, query_name: str, sql: str, parameters: Union[List, Dict]
    ) -> Optional[Any]:
        ...

    def execute_script(self, conn: Any, sql: str) -> None:
        ...