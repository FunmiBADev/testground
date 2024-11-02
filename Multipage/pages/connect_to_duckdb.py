import duckdb
import os
import pandas as pd
from datetime import datetime
from typing import Optional

class ConnectToDuckDB:
    def __init__(self, storage_account: str, container: str, connection_string: str):
        self.storage_account = storage_account
        self.container = container
        self.connection_string = connection_string
        os.environ['AZURE_STORAGE_CONNECTION_STRING'] = connection_string

    def get_daily_jre_by_date(self, date_str: str) -> Optional[pd.DataFrame]:
        # Validate and format the date string
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in 'YYYY-MM-DD' format")
        
        # Connect to DuckDB and query the Parquet file for the specified date
        conn = duckdb.connect()
        query = f"""
        SELECT *
        FROM read_parquet(
            'azure://{self.container}/{date_str}.parquet',
            connection_string=$AZURE_STORAGE_CONNECTION_STRING
        )
        """
        
        try:
            # Execute the query and fetch results as a DataFrame
            result_df = conn.execute(query).fetchdf()
        except Exception as e:
            print(f"Failed to retrieve data for date {date_str}: {e}")
            return None
        finally:
            conn.close()
        
        return result_df
