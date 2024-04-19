// GEM
from gitlab import Gitlab
import re

def search_gitlab_ci_yml(gitlab_url, private_token):
  """Searches GitLab projects for .yml files and checks for 'includes: scan_build_template'.

  Args:
      gitlab_url (str): The base URL of your GitLab instance (e.g., "https://gitlab.com").
      private_token (str): The GitLab access token with read permissions.

  Returns:
      list: A list of dictionaries containing project names and .yml file names that don't include 'scan_build_template'.
  """

  gl = Gitlab(gitlab_url, private_token=private_token)

  # Use pagination to retrieve all projects efficiently
  all_project_info = []
  page = 1
  per_page = 100  # Adjust this value as needed

  while True:
    projects = gl.projects.list(page=page, per_page=per_page)
    if not projects:
      break

    for project in projects:
      # Get the content of .gitlab-ci.yml file (assuming this is the file you want to search)
      try:
        content = project.files.get(".gitlab-ci.yml").content
        # Check for 'includes: scan_build_template' using regular expressions
        if not re.search(rf"^{'includes:.*scan_build_template'}", content, flags=re.MULTILINE):
          all_project_info.append({"project_name": project.name, "file_name": ".gitlab-ci.yml"})
      except GitlabGetError as e:
        if e.response_code == 404:  # File not found, ignore
          pass
        else:
          raise e  # Re-raise other errors

    page += 1

  return all_project_info

# Replace with your actual values
gitlab_url = "https://gitlab.com"
private_token = os.environ.get("GITLAB_ACCESS_TOKEN")

# Get project and file information
project_and_file_info = search_gitlab_ci_yml(gitlab_url, private_token)

# Print information
if project_and_file_info:
  print("Projects and .yml files that don't include 'scan_build_template':")
  for info in project_and_file_info:
    print(f"- Project: {info['project_name']}, File: {info['file_name']}")
else:
  print("No projects or .yml files found that don't include 'scan_build_template'.")


// JAGUAR

import os
from gitlab import Gitlab

def search_yaml_files_for_keyword(project, keyword):
    try:
        yaml_files = project.repository_tree(recursive=True, all=True, path='/', ref='master', as_list=True)

        for yaml_file in yaml_files:
            if yaml_file['name'].endswith('.yml'):
                file_content = project.files.raw(file_path=yaml_file['path'], ref='master')
                if 'includes' in file_content and keyword in file_content['includes']:
                    print(f"Project: {project.name}, YAML file: {yaml_file['name']}")
    except Exception as e:
        print(f"Failed to search YAML files for project {project.name}. Error: {e}")

def search_projects_for_keyword(projects, keyword):
    for project in projects:
        search_yaml_files_for_keyword(project, keyword)

if __name__ == "__main__":
    token = os.environ.get('GITLAB_PRIVATE_TOKEN')
    if not token:
        print("Error: GitLab private access token not found in environment variables.")
    else:
        gl = Gitlab('https://gitlab.com', private_token=token)
        projects = gl.projects.list(all=True)
        
        keyword = input("Enter the keyword to search for in 'includes' section: ")

        search_projects_for_keyword(projects, keyword)


// Jaguar namescape search

if __name__ == "__main__":
    token = os.environ.get('GITLAB_PRIVATE_TOKEN')
    if not token:
        print("Error: GitLab private access token not found in environment variables.")
    else:
        gl = Gitlab('https://gitlab.com', private_token=token)
        namespace = input("Enter the namespace: ")
        
        # Fetch projects within the specified namespace only
        projects = gl.projects.list(search=namespace)

        keyword = input("Enter the keyword to search for in 'includes' section: ")

        search_projects_for_keyword(projects, keyword)
