import pandas as pd

replace_jre = ["1.8_601", "1.8_253", "1.8_765", "1.8_453"]

def check_jre_change(prev_excel_file, curr_excel_file):
    """
    Compare previous and current versions of a DataFrame from Excel files and 
    count the occurrences of specified 'jre' values.
    
    Parameters:
        prev_excel_file (str): File path to the previous version of the Excel file.
        curr_excel_file (str): File path to the current version of the Excel file.
        
    Returns:
        dict: A dictionary containing the counts of specified 'jre' values in the previous and current versions.
    """
    # Load previous and current DataFrames from Excel files
    prev_df = pd.read_excel(prev_excel_file)
    curr_df = pd.read_excel(curr_excel_file)
    
    # Filter DataFrames to contain only necessary columns
    prev_df = prev_df[['name', 'host', 'jre']]
    curr_df = curr_df[['name', 'host', 'jre']]
    
    # Check for replace_jre in 'jre' column
    prev_count = prev_df['jre'].apply(lambda x: any(jre in x for jre in replace_jre)).sum()
    curr_count = curr_df['jre'].apply(lambda x: any(jre in x for jre in replace_jre)).sum()
    
    # Create a dictionary to hold the results
    change_info = {
        'previous_count': prev_count,
        'current_count': curr_count
    }
    
    return change_info

# Example usage:
prev_excel_file = "previous_version.xlsx"
curr_excel_file = "current_version.xlsx"

change_info = check_jre_change(prev_excel_file, curr_excel_file)
print("Previous Version Count:", change_info['previous_count'])
print("Current Version Count:", change_info['current_count'])


import pandas as pd

replace_jre = ["1.8_601", "1.8_253", "1.8_765", "1.8_453"]

def check_jre_change(prev_json_file, curr_json_file):
    """
    Compare previous and current versions of a DataFrame from JSON files and 
    count the occurrences of specified 'jre' values.
    
    Parameters:
        prev_json_file (str): File path to the previous version of the JSON file.
        curr_json_file (str): File path to the current version of the JSON file.
        
    Returns:
        dict: A dictionary containing the counts of specified 'jre' values in the previous and current versions.
    """
    # Load previous and current DataFrames from JSON files
    prev_df = pd.read_json(prev_json_file)
    curr_df = pd.read_json(curr_json_file)
    
    # Filter DataFrames to contain only necessary columns
    prev_df = prev_df[['name', 'host', 'jre']]
    curr_df = curr_df[['name', 'host', 'jre']]
    
    # Check for replace_jre in 'jre' column
    prev_count = prev_df['jre'].apply(lambda x: any(jre in x for jre in replace_jre)).sum()
    curr_count = curr_df['jre'].apply(lambda x: any(jre in x for jre in replace_jre)).sum()
    
    # Create a dictionary to hold the results
    change_info = {
        'previous_count': prev_count,
        'current_count': curr_count
    }
    
    return change_info

# Example usage:
prev_json_file = "previous_version.json"
curr_json_file = "current_version.json"

change_info = check_jre_change(prev_json_file, curr_json_file)
print("Previous Version Count:", change_info['previous_count'])
print("Current Version Count:", change_info['current_count'])
