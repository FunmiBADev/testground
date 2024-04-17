// Jaguar without gitlab library
import os
import requests

def get_all_projects():
    token = os.environ.get('GITLAB_PRIVATE_TOKEN')
    if not token:
        print("Error: GitLab private access token not found in environment variables.")
        return
    
    headers = {'Private-Token': token}
    url = "https://gitlab.com/api/v4/projects"
    params = {'per_page': 100}  # Adjust per_page as needed to fetch more projects
    
    projects = []
    page = 1
    while True:
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Failed to fetch projects. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            break
        
        page_projects = response.json()
        if not page_projects:
            break
        
        projects.extend(page_projects)
        page += 1
    
    return projects

def update_ci_file(project_id, token):
    headers = {'Private-Token': token}
    url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/files/.gitlab-ci.yml/raw"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch .gitlab-ci.yml for project ID {project_id}. Status code: {response.status_code}")
        return

    ci_content = response.text

    if 'scan_build_templates' in ci_content:
        print(f".gitlab-ci.yml in project ID {project_id} already includes scan_build_templates")
        return

    updated_ci_content = ci_content.strip() + '\n\nincludes:\n  - scan_build_templates\n'
    
    update_url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/files/.gitlab-ci.yml"
    data = {
        'branch': 'master',
        'content': updated_ci_content,
        'commit_message': 'Add scan_build_templates to .gitlab-ci.yml'
    }
    response = requests.put(update_url, headers=headers, data=data)
    
    if response.status_code == 200:
        print(f".gitlab-ci.yml in project ID {project_id} updated successfully!")
    else:
        print(f"Failed to update .gitlab-ci.yml for project ID {project_id}. Status code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    projects = get_all_projects()
    for project in projects:
        project_id = project['id']
        token = os.environ.get('GITLAB_PRIVATE_TOKEN')
        if token:
            update_ci_file(project_id, token)
        else:
            print("Error: GitLab private access token not found in environment variables.")
            break


// Jaguar gitlab library
import os
from gitlab import Gitlab

def get_all_projects():
    token = os.environ.get('GITLAB_PRIVATE_TOKEN')
    if not token:
        print("Error: GitLab private access token not found in environment variables.")
        return []
    
    gl = Gitlab('https://gitlab.com', private_token=token)
    projects = gl.projects.list(all=True)
    return projects

def update_ci_file(project):
    try:
        ci_file = project.files.get(file_path='.gitlab-ci.yml', ref='master')
        ci_content = ci_file.decode()
        
        if 'scan_build_templates' in ci_content:
            print(f".gitlab-ci.yml in project ID {project.id} already includes scan_build_templates")
            return
        
        updated_ci_content = ci_content.strip() + '\n\nincludes:\n  - scan_build_templates\n'
        ci_file.content = updated_ci_content
        ci_file.save(branch='master', commit_message='Add scan_build_templates to .gitlab-ci.yml')
        print(f".gitlab-ci.yml in project ID {project.id} updated successfully!")
    except Exception as e:
        print(f"Failed to update .gitlab-ci.yml for project ID {project.id}. Error: {e}")

if __name__ == "__main__":
    projects = get_all_projects()
    for project in projects:
        update_ci_file(project)

// GEM

from gitlab import Gitlab
import re

def update_gitlab_ci_yml(gitlab_url, private_token, project_id, branch_name, include_line):
  """Updates a GitLab project's gitlab-ci.yml file with the specified include line.

  Args:
      gitlab_url (str): The base URL of your GitLab instance (e.g., "https://gitlab.com").
      private_token (str): The GitLab access token with write permissions.
      project_id (int): The ID of the project.
      branch_name (str): The branch name containing the gitlab-ci.yml file.
      include_line (str): The include line to add (e.g., "includes: scan_build_templates").

  Returns:
      bool: True if the file was updated, False otherwise.
  """

  gl = Gitlab(gitlab_url, private_token=private_token)
  project = gl.projects.get(project_id)

  try:
    # Get the content of gitlab-ci.yml
    content = project.files.get("gitlab-ci.yml").content

    # Check if the include line already exists
    if not re.search(rf"^{include_line}$", content, flags=re.MULTILINE):
      # Add the include line at the beginning
      content = f"{include_line}\n{content}"

      # Update the file
      project.files.update("gitlab-ci.yml", content=content, branch_name=branch_name)
      print(f"Updated gitlab-ci.yml for project ID: {project_id} (branch: {branch_name})")
      return True
    else:
      print(f"gitlab-ci.yml already includes: {include_line} (project ID: {project_id}, branch: {branch_name})")
      return False

  except Exception as e:
    print(f"Error updating gitlab-ci.yml for project ID: {project_id} (branch: {branch_name}) - {e}")
    return False

# Replace with your actual values
gitlab_url = "https://gitlab.com"
private_token = os.environ.get("GITLAB_ACCESS_TOKEN")
include_line = "includes: scan_build_templates"

# Get all project IDs (consider using the script from previous response)
project_ids = [12345, 67890]  # Replace with your actual project IDs

# Loop through projects and update files
for project_id in project_ids:
  # Assume all projects have gitlab-ci.yml on the default branch (modify as needed)
  updated = update_gitlab_ci_yml(gitlab_url, private_token, project_id, "master", include_line)
  if not updated:
    print(f"Project ID: {project_id} might not have a gitlab-ci.yml file or there might be errors retrieving it.")

