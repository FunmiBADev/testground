from gitlab import Gitlab
import re

def search_gitlab_ci_yml_in_group(gitlab_url, private_token, group_id):
  """Searches GitLab projects within a specific group for .yml files and checks for 'includes: scan_build_template'.

  Args:
      gitlab_url (str): The base URL of your GitLab instance (e.g., "https://gitlab.com").
      private_token (str): The GitLab access token with read permissions.
      group_id (int): The ID of the GitLab group to search within.

  Returns:
      list: A list of dictionaries containing project names and .yml file names that don't include 'scan_build_template'.
  """

  gl = Gitlab(gitlab_url, private_token=private_token)

  # Get projects within the specified group
  projects = gl.groups.get(group_id).projects.list(all=True)  # Use all=True to retrieve all projects

  all_project_info = []
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

  return all_project_info

# Replace with your actual values
gitlab_url = "https://gitlab.com"
private_token = os.environ.get("GITLAB_ACCESS_TOKEN")
group_id = 1234  # Replace with your actual group ID

# Get project and file information
project_and_file_info = search_gitlab_ci_yml_in_group(gitlab_url, private_token, group_id)

# Print information
if project_and_file_info:
  print("Projects and .yml files that don't include 'scan_build_template':")
  for info in project_and_file_info:
    print(f"- Project: {info['project_name']}, File: {info['file_name']}")
else:
  print("No projects or .yml files found that don't include 'scan_build_template' within the specified group.")
