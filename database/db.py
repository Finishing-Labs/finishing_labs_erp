"""
Database Utility - Raw SQL execution with psycopg

Usage:
    DB.query(sql, params)              # Returns all rows
    DB.fetch_one(sql, params)          # Returns single row
    DB.fetch_value(sql, params)        # Returns single value
    DB.execute(sql, params)            # INSERT/UPDATE/DELETE
    DB.execute_returning_id(sql, params)  # Returns generated ID
    with DB.transaction(): ...         # Manual transaction
"""

import os
import psycopg
from contextlib import contextmanager


class DatabaseConnection:
    """Manages PostgreSQL connection with auto-reconnect"""
    
    def __init__(self):
        self._connection = None
        self._database_url = None
    
    def _get_connection_params(self):
        """Get connection params from DATABASE_URL or individual env vars"""
        database_url = os.environ.get('DATABASE_URL')
        
        if database_url:
            if database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
            return database_url
        return {
            'dbname': os.environ.get('DB_NAME', 'finishing_labs_erp'),
            'user': os.environ.get('DB_USER', 'postgres'),
            'password': os.environ.get('DB_PASSWORD', 'postgres'),
            'host': os.environ.get('DB_HOST', 'localhost'),
            'port': os.environ.get('DB_PORT', '5432')
        }
    
    def get_connection(self):
        """Get active connection, create if needed"""
        if self._connection is None or self._connection.closed:
            params = self._get_connection_params()
            
            if isinstance(params, str):
                self._connection = psycopg.connect(params)
            else:
                self._connection = psycopg.connect(**params)
            
            self._connection.autocommit = True
        
        return self._connection
    
    def close(self):
        """Close connection"""
        if self._connection and not self._connection.closed:
            self._connection.close()
            self._connection = None


_db_connection = DatabaseConnection()


class DB:
    """Static database utility for SQL execution"""
    
    @staticmethod
    def query(sql, params=None):
        """Execute query, return all rows as list of dicts"""
        conn = _db_connection.get_connection()
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or [])
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()
                return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            print(f"Database query error: {e}")
            print(f"SQL: {sql}")
            print(f"Params: {params}")
            raise
    
    @staticmethod
    def fetch_one(sql, params=None):
        """Execute query, return single row as dict or None"""
        conn = _db_connection.get_connection()
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or [])
                result = cursor.fetchone()
                if result:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, result))
                return None
        except Exception as e:
            print(f"Database query error: {e}")
            print(f"SQL: {sql}")
            print(f"Params: {params}")
            raise
    
    @staticmethod
    def fetch_value(sql, params=None):
        """Execute query, return single value (first column of first row)"""
        conn = _db_connection.get_connection()
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or [])
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            print(f"Database query error: {e}")
            print(f"SQL: {sql}")
            print(f"Params: {params}")
            raise
    
    @staticmethod
    def execute(sql, params=None):
        """Execute INSERT/UPDATE/DELETE, return affected row count"""
        conn = _db_connection.get_connection()
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or [])
                return cursor.rowcount
        except Exception as e:
            print(f"Database execution error: {e}")
            print(f"SQL: {sql}")
            print(f"Params: {params}")
            raise
    
    @staticmethod
    def execute_returning_id(sql, params=None):
        """Execute INSERT with RETURNING clause, return generated ID"""
        conn = _db_connection.get_connection()
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or [])
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            print(f"Database execution error: {e}")
            print(f"SQL: {sql}")
            print(f"Params: {params}")
            raise
    
    @staticmethod
    @contextmanager
    def transaction():
        """Transaction context: commits on success, rolls back on error"""
        conn = _db_connection.get_connection()
        old_autocommit = conn.autocommit
        conn.autocommit = False
        
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.autocommit = old_autocommit
    
    @staticmethod
    def close():
        """Close connection"""
        _db_connection.close()


def init_db(app):
    """Initialize DB with Flask app (connection lazy-loaded on first query)"""
    pass


def close_db(error=None):
    """Close DB connection (call on app teardown)"""
    DB.close()
