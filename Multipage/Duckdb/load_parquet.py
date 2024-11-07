import duckdb
from azure.storage.blob import ContainerClient
import pandas as pd

def load_partitioned_parquet_from_azure(storage_account_name: str, container_name: str, prefix: str, sas_token: str):
    # Initialize DuckDB connection
    conn = duckdb.connect()
    
    # Enable the HTTPFS extension for remote file access
    conn.execute("INSTALL httpfs;")
    conn.execute("LOAD httpfs;")
    
    # Construct the URL for the Azure Blob Storage container
    blob_service_url = f"https://{storage_account_name}.blob.core.windows.net"
    container_client = ContainerClient(
        account_url=blob_service_url,
        container_name=container_name,
        credential=sas_token
    )
    
    # List all Parquet files in the specified partitioned path
    parquet_files = []
    for blob in container_client.list_blobs(name_starts_with=prefix):
        if blob.name.endswith(".parquet"):
            parquet_files.append(f"{blob_service_url}/{container_name}/{blob.name}{sas_token}")

    # Check if any files were found
    if not parquet_files:
        print("No parquet files found in the specified path.")
        return pd.DataFrame()

    # Read all Parquet files using DuckDB
    query = f"SELECT * FROM read_parquet({parquet_files});"
    result_df = conn.execute(query).fetchdf()
    
    # Close the connection
    conn.close()
    
    return result_df

# Example usage
# data_df = load_partitioned_parquet_from_azure("your_storage_account", "your_container_name", "prefix/year/month/date", "?<your_sas_token>")
# print(data_df)
