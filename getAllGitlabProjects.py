import os
import requests
//Jaguar
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

if __name__ == "__main__":
    projects = get_all_projects()
    print("GitLab Projects:")
    for project in projects:
        print(f"ID: {project['id']}, Name: {project['name']}, Path: {project['path_with_namespace']}")


// GEM
from gitlab import Gitlab

def get_all_project_ids(gitlab_url, private_token):
  """Searches and returns a list of all GitLab project IDs.

  Args:
      gitlab_url (str): The base URL of your GitLab instance (e.g., "https://gitlab.com").
      private_token (str): The GitLab access token with read permissions.

  Returns:
      list: A list of all GitLab project IDs.
  """

  gl = Gitlab(gitlab_url, private_token=private_token)

  # Use pagination to retrieve all projects efficiently
  all_project_ids = []
  page = 1
  per_page = 100  # Adjust this value as needed

  while True:
    projects = gl.projects.list(page=page, per_page=per_page)
    if not projects:
      break

    all_project_ids.extend([project.id for project in projects])
    page += 1

  return all_project_ids

# Replace with your actual values
gitlab_url = "https://gitlab.com"
private_token = os.environ.get("GITLAB_ACCESS_TOKEN")

# Get all project IDs
project_ids = get_all_project_ids(gitlab_url, private_token)

# Print all project IDs
print(project_ids)

