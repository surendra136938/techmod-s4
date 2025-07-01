import psycopg2
from psycopg2 import OperationalError, Error
from typing import Optional, List, Dict, Any, Tuple, Union
from app.services.moveservice import MoveService

class PgSqlDAO:
    """PostgreSQL data access object for database operations."""
    
    def __init__(
        self, 
        db_host: str, 
        db_user: str, 
        db_password: str, 
        s4_database_name: str, 
        db_port: int = 5432
    ) -> None:
        """Initialize PostgreSQL connection with provided credentials."""
        self.db = None
        try:
            self.db = psycopg2.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                dbname=s4_database_name,
                port=db_port
            )
            MoveService.log_info(f"db_host=>{db_host}")
        except OperationalError as e:
            MoveService.log_error(f"Failed to connect to PostgreSQL: {e}")
            self.db = None

    def insert(self, insert_statement: str, params: Tuple[Any, ...]) -> None:
        """Execute an INSERT SQL statement with parameters."""
        MoveService.log_info(f"Calling PgSqlDAO::insert(), executing sql insert statement: {insert_statement}")
        if params:
            for idx, val in enumerate(params, 1):
                MoveService.log_info(f"binding param {idx} = {val}")
        if not self.db:
            MoveService.log_error("No valid connection to PostgreSQL db!!!")
            return
        cursor = self.db.cursor()
        try:
            cursor.execute(insert_statement, params)
            self.db.commit()
        except Error as e:
            MoveService.log_error(f"PgSqlDAO::insert() error: {e}")
        finally:
            cursor.close()

    def update(self, update_statement: str, params: Tuple[Any, ...]) -> None:
        """Execute an UPDATE SQL statement with parameters."""
        MoveService.log_info(f"Calling PgSqlDAO::update(), executing sql update statement: {update_statement}")
        if params:
            for idx, val in enumerate(params, 1):
                MoveService.log_info(f"binding param {idx} = {val}")
        if not self.db:
            MoveService.log_error("No valid connection to PostgreSQL db!!!")
            return
        cursor = self.db.cursor()
        try:
            cursor.execute(update_statement, params)
            self.db.commit()
        except Error as e:
            MoveService.log_error(f"PgSqlDAO::update() error: {e}")
        finally:
            cursor.close()

    def get(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dictionaries."""
        MoveService.log_info(f"Calling PgSqlDAO::get(), executing sql query: {query}")
        if params:
            for idx, val in enumerate(params, 1):
                MoveService.log_info(f"binding param {idx} = {val}")
        result = []
        if not self.db:
            MoveService.log_error("No valid connection to PostgreSQL db!!!")
            return result
        cursor = self.db.cursor()
        try:
            cursor.execute(query, params or ())
            columns = [desc[0] for desc in cursor.description]
            for row in cursor.fetchall():
                result.append(dict(zip(columns, row)))
        except Error as e:
            MoveService.log_error(f"PgSqlDAO::get() error: {e}")
        finally:
            cursor.close()
        return result

    def delete(self, delete_statement: str, params: Tuple[Any, ...]) -> None:
        """Execute a DELETE SQL statement with parameters."""
        MoveService.log_info(f"Calling PgSqlDAO::delete(), executing sql delete statement: {delete_statement}")
        if params:
            for idx, val in enumerate(params, 1):
                MoveService.log_info(f"binding param {idx} = {val}")
        if not self.db:
            MoveService.log_error("No valid connection to PostgreSQL db!!!")
            return
        cursor = self.db.cursor()
        try:
            cursor.execute(delete_statement, params)
            self.db.commit()
        except Error as e:
            MoveService.log_error(f"PgSqlDAO::delete() error: {e}")
        finally:
            cursor.close()

    def close(self) -> None:
        """Close the database connection."""
        if self.db:
            self.db.close()

