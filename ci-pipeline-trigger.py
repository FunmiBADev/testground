""""Jaguar without gitlab library""""
import os
import requests

def trigger_pipeline(project_ids, ref='master'):
    token = os.environ.get('GITLAB_PRIVATE_TOKEN')
    if not token:
        print("Error: GitLab private access token not found in environment variables.")
        return
    
    headers = {'Private-Token': token}
    data = {'ref': ref}
    
    for project_id in project_ids:
        url = f"https://gitlab.com/api/v4/projects/{project_id}/trigger/pipeline"
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 201:
            print(f"Pipeline triggered successfully for project ID {project_id}!")
        else:
            print(f"Failed to trigger pipeline for project ID {project_id}. Status code: {response.status_code}")
            print(f"Response: {response.text}")

if __name__ == "__main__":
    project_ids_input = input("Enter your GitLab project IDs separated by commas: ")
    project_ids = [int(id.strip()) for id in project_ids_input.split(',')]
    ref = input("Enter the branch or tag name (default: master): ") or 'master'
    
    trigger_pipeline(project_ids, ref)

"""" Jaguar with gitlab library
""""
import os
from gitlab import Gitlab

def trigger_pipeline(project_ids, ref='master'):
    token = os.environ.get('GITLAB_PRIVATE_TOKEN')
    if not token:
        print("Error: GitLab private access token not found in environment variables.")
        return
    
    gl = Gitlab('https://gitlab.com', private_token=token)
    
    for project_id in project_ids:
        try:
            project = gl.projects.get(project_id)
            pipeline = project.pipelines.create({'ref': ref})
            print(f"Pipeline triggered successfully for project ID {project_id}!")
        except Exception as e:
            print(f"Failed to trigger pipeline for project ID {project_id}. Error: {e}")

if __name__ == "__main__":
    project_ids_input = input("Enter your GitLab project IDs separated by commas: ")
    project_ids = [int(id.strip()) for id in project_ids_input.split(',')]
    ref = input("Enter the branch or tag name (default: master): ") or 'master'
    
    trigger_pipeline(project_ids, ref)


""""GEM""""
import requests

def trigger_gitlab_pipeline(gitlab_url, project_id, branch_name, token):
  """Triggers a GitLab CI pipeline for a specific project and branch.

  Args:
      gitlab_url (str): The base URL of your GitLab instance (e.g., "https://gitlab.com").
      project_id (int): The ID of the project.
      branch_name (str): The branch name for which to trigger the pipeline.
      token (str): The GitLab access token with pipeline trigger permissions.
  """

  headers = {"Private-Token": token}
  url = f"{gitlab_url}/api/v4/projects/{project_id}/trigger/pipeline"
  data = {"ref": branch_name}

  try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for non-2xx status codes

    print(f"Successfully triggered pipeline for project ID {project_id} (branch: {branch_name})")
  except requests.exceptions.RequestException as e:
    print(f"Error triggering pipeline: {e}")

# Replace these variables with your actual values
gitlab_url = "https://gitlab.com"
token = os.environ.get("GITLAB_ACCESS_TOKEN")

# List of projects (project_id, branch_name) tuples
projects = [
  (12345, "master"),
  (67890, "development"),
  # Add more project IDs and branch names as needed
]

# Trigger pipelines for each project
for project_id, branch_name in projects:
  trigger_gitlab_pipeline(gitlab_url, project_id, branch_name, token)

# GEM using Gitlab Library

from gitlab import Gitlab

def trigger_gitlab_pipeline(gitlab_url, private_token, project_id, branch_name):
  """Triggers a GitLab CI pipeline for a specific project and branch using the python-gitlab library.

  Args:
      gitlab_url (str): The base URL of your GitLab instance (e.g., "https://gitlab.com").
      private_token (str): The GitLab access token with pipeline trigger permissions.
      project_id (int): The ID of the project.
      branch_name (str): The branch name for which to trigger the pipeline.
  """

  gl = Gitlab(gitlab_url, private_token=private_token)
  project = gl.projects.get(project_id)

  try:
    # Trigger pipeline using GitLab instance
    pipeline = project.pipelines.create({"ref": branch_name})
    print(f"Successfully triggered pipeline for project ID {project_id} (branch: {branch_name}) - Pipeline ID: {pipeline.id}")
  except GitlabGetError as e:
    print(f"Error triggering pipeline: {e}")

# Replace with your actual values
gitlab_url = "https://gitlab.com"
# Prompt for private token securely
private_token = getpass("Enter your GitLab private token (will not be displayed): ")

private_token = os.environ.get("GITLAB_ACCESS_TOKEN")

# List of projects (project_id, branch_name) tuples
projects = [
  (12345, "master"),
  (67890, "development"),
  # Add more project IDs and branch names as needed
]

# Trigger pipelines for each project
for project_id, branch_name in projects:
  trigger_gitlab_pipeline(gitlab_url, private_token, project_id, branch_name)
