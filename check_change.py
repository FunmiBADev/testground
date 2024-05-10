import pandas as pd

def check_change(prev_excel_file, curr_excel_file):
    """
    Compare previous and current versions of a DataFrame from Excel files and 
    look up the change in 'jre' information where 'ASSEMBLY = jre-openjdk'.
    
    Parameters:
        prev_excel_file (str): File path to the previous version of the Excel file.
        curr_excel_file (str): File path to the current version of the Excel file.
        
    Returns:
        dict: A dictionary containing the change in 'jre' information and the count of changes.
    """
    # Load previous and current DataFrames from Excel files
    prev_df = pd.read_excel(prev_excel_file)
    curr_df = pd.read_excel(curr_excel_file)
    
    # Filter DataFrames to contain only necessary columns
    prev_df = prev_df[['name', 'host', 'jre']]
    curr_df = curr_df[['name', 'host', 'jre']]
    
    # Find the change in 'jre' information where 'ASSEMBLY = jre-openjdk'
    prev_jre_openjdk_count = prev_df.loc[prev_df['jre'].str.contains('ASSEMBLY = jre-openjdk', na=False)].shape[0]
    curr_jre_openjdk_count = curr_df.loc[curr_df['jre'].str.contains('ASSEMBLY = jre-openjdk', na=False)].shape[0]
    
    # Create a dictionary to hold the results
    change_info = {
        'previous_version': prev_df.loc[prev_df['jre'].str.contains('ASSEMBLY = jre-openjdk', na=False)],
        'current_version': curr_df.loc[curr_df['jre'].str.contains('ASSEMBLY = jre-openjdk', na=False)],
        'previous_count': prev_jre_openjdk_count,
        'current_count': curr_jre_openjdk_count
    }
    
    return change_info

# Example usage:
prev_excel_file = "previous_version.xlsx"
curr_excel_file = "current_version.xlsx"

change_info = check_change(prev_excel_file, curr_excel_file)
print("Previous Version with 'ASSEMBLY = jre-openjdk':")
print(change_info['previous_version'])
print("Previous Version Count:", change_info['previous_count'])
print("\nCurrent Version with 'ASSEMBLY = jre-openjdk':")
print(change_info['current_version'])
print("Current Version Count:", change_info['current_count'])
