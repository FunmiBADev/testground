import gitlab

def search_yaml_files(gl, group_id, file_paths):
  """
  Searches for .yml files in projects within a group and specified file paths.

  Args:
      gl (gitlab.Gitlab): Gitlab API instance.
      group_id (str): ID of the group to search within.
      file_paths (list): List of file paths to search in (e.g., ["path/to/file1", "path/to/folder"]).
  """
  projects = gl.groups.get(group_id).projects.list(all=True)

  for project in projects:
    for file_path in file_paths:
      try:
        # Build the full file path within the project
        full_path = os.path.join(project.path_with_namespace, file_path)

        # Get the file content (if it exists)
        file_content = project.files.raw(file_path=full_path, ref='master')

        # Print information if the file is a .yml file
        if file_content and file_content.endswith('.yml'):
          print(f"Project: {project.name}")
          print(f"File Path: {full_path}")
          print(f"File Name: {os.path.basename(full_path)}")
          print(f"File Content:\n{file_content}\n")

      except Exception as e:
        print(f"Error accessing file {full_path} in project {project.name}: {e}")

if __name__ == "__main__":
  # Replace with your Gitlab private token (set as environment variable)
  token = os.environ.get('GITLAB_PRIVATE_TOKEN')
  if not token:
    print("Error: GitLab private access token not found in environment variables.")
    exit()

  # Replace with your group ID
  group_id = "YOUR_GROUP_ID"

  # Replace with a list of file paths to search (modify as needed)
  file_paths = ["path/to/file1.yml", "path/to/folder/"]

  # Create Gitlab API instance
  gl = gitlab.Gitlab('https://gitlab.com', private_token=token)

  # Initiate search
  search_yaml_files(gl, group_id, file_paths)

import gitlab

def print_project_tree(gl, project_id, recursive=True):
  """
  Prints the repository tree for a project, optionally recursively.

  Args:
      gl (gitlab.Gitlab): Gitlab API instance.
      project_id (str): ID of the project.
      recursive (bool, optional): Whether to print the tree recursively (default: True).
  """
  try:
    project = gl.projects.get(project_id)
    tree = project.repository_tree(recursive=recursive, all=True)

    for item in tree:
      # Print file name or directory name
      if item['type'] == 'blob':
        print(f"- File: {item['name']}")
      else:
        print(f"- Directory: {item['name']}")

      # Recursively print subdirectories (if enabled)
      if recursive and item['type'] == 'tree':
        print_project_tree(gl, item['id'], recursive)

  except Exception as e:
    print(f"Error accessing project {project_id}: {e}")

if __name__ == "__main__":
  # Replace with your Gitlab private token (set as environment variable)
  token = os.environ.get('GITLAB_PRIVATE_TOKEN')
  if not token:
    print("Error: GitLab private access token not found in environment variables.")
    exit()

  # Replace with your group ID
  group_id = "YOUR_GROUP_ID"

  # Create Gitlab API instance
  gl = gitlab.Gitlab('https://gitlab.com', private_token=token)

  # Retrieve projects within the group
  projects = gl.groups.get(group_id).projects.list(all=True)

  # Print tree for each project
  for project in projects:
    print(f"\nProject: {project.name}")
    print_project_tree(gl, project.id)

