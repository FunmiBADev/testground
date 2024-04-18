# Jaguar

import os
from gitlab import Gitlab

def update_ci_file(project):
    try:
        # Check if .gitlab-ci.yml exists
        ci_file = project.files.get(file_path='.gitlab-ci.yml', ref='master')
        ci_content = ci_file.decode()

        # Check if .gitlab-ci.yml contains scan_build_templates
        if 'scan_build_templates' not in ci_content:
            # Create a new branch called 'newBrachName'
            new_branch = project.branches.create({'branch': 'newBrachName', 'ref': 'master'})

            # Update .gitlab-ci.yml file
            updated_ci_content = ci_content.strip() + '\n\nincludes:\n  - scan_build_templates\n'
            project.files.create({'file_path': '.gitlab-ci.yml', 'branch': 'newBrachName', 'content': updated_ci_content, 'commit_message': 'Add scan_build_templates to .gitlab-ci.yml'})

            print(f".gitlab-ci.yml in project ID {project.id} updated successfully!")
        else:
            print(f".gitlab-ci.yml in project ID {project.id} already includes scan_build_templates")
    except Exception as e:
        print(f"Failed to update .gitlab-ci.yml for project ID {project.id}. Error: {e}")

if __name__ == "__main__":
    token = os.environ.get('GITLAB_PRIVATE_TOKEN')
    if not token:
        print("Error: GitLab private access token not found in environment variables.")
    else:
        gl = Gitlab('https://gitlab.com', private_token=token)
        projects = gl.projects.list(all=True)

        for project in projects:
            update_ci_file(project)
            
# JAGUAR Multi projects create

import os
from gitlab import Gitlab
from multiprocessing import Pool

def update_ci_file(project_id, token):
    try:
        gl = Gitlab('https://gitlab.com', private_token=token)
        project = gl.projects.get(project_id)

        # Check if .gitlab-ci.yml exists
        ci_file = project.files.get(file_path='.gitlab-ci.yml', ref='master')
        ci_content = ci_file.decode()

        # Check if .gitlab-ci.yml contains scan_build_templates
        if 'scan_build_templates' not in ci_content:
            # Create a new branch called 'vm15Scanner'
            new_branch = project.branches.create({'branch': 'vm15Scanner', 'ref': 'master'})

            # Update .gitlab-ci.yml file
            updated_ci_content = ci_content.strip() + '\n\nincludes:\n  - scan_build_templates\n'
            project.files.create({'file_path': '.gitlab-ci.yml', 'branch': 'vm15Scanner', 'content': updated_ci_content, 'commit_message': 'Add scan_build_templates to .gitlab-ci.yml'})

            print(f".gitlab-ci.yml in project ID {project_id} updated successfully!")
        else:
            print(f".gitlab-ci.yml in project ID {project_id} already includes scan_build_templates")
    except Exception as e:
        print(f"Failed to update .gitlab-ci.yml for project ID {project_id}. Error: {e}")

def main():
    token = os.environ.get('GITLAB_PRIVATE_TOKEN')
    if not token:
        print("Error: GitLab private access token not found in environment variables.")
        return

    project_ids_input = input("Enter your GitLab project IDs separated by commas: ")
    project_ids = [int(id.strip()) for id in project_ids_input.split(',')]

    # Create a pool of processes to update projects concurrently
    with Pool() as pool:
        pool.starmap(update_ci_file, [(project_id, token) for project_id in project_ids])

if __name__ == "__main__":
    main()


# GEM

from gitlab import Gitlab
import re

def update_gitlab_ci_yml_with_scan_build_templates(gitlab_url, private_token, project_id, branch_name, scan_build_templates_include):
  """Updates a GitLab project's gitlab-ci.yml file with the specified include line if not already present.

  Args:
      gitlab_url (str): The base URL of your GitLab instance (e.g., "https://gitlab.com").
      private_token (str): The GitLab access token with write permissions.
      project_id (int): The ID of the project.
      branch_name (str): The branch name containing the gitlab-ci.yml file.
      scan_build_templates_include (str): The include line to add (e.g., "includes: scan_build_templates").

  Returns:
      bool: True if the file was updated, False otherwise.
  """

  gl = Gitlab(gitlab_url, private_token=private_token)
  project = gl.projects.get(project_id)

  try:
    # Get the content of gitlab-ci.yml
    content = project.files.get("gitlab-ci.yml").content

    # Check if the include line already exists
    if not re.search(rf"^{scan_build_templates_include}$", content, flags=re.MULTILINE):
      # Add the include line at the beginning
      content = f"{scan_build_templates_include}\n{content}"

      # Create a new branch named 'vm15Scanner' if it doesn't exist
      try:
        project.branches.create({"branch_name": "vm15Scanner"})
        print(f"Created branch 'vm15Scanner' for project ID: {project_id}")
      except GitlabGetError as e:
        if e.response_code == 409:  # Branch already exists
          print(f"Branch 'vm15Scanner' already exists for project ID: {project_id}")
        else:
          raise e  # Re-raise other errors

      # Update the file in the 'vm15Scanner' branch
      project.files.update("gitlab-ci.yml", content=content, branch_name="vm15Scanner")
      print(f"Updated gitlab-ci.yml for project ID: {project_id} (branch: vm15Scanner)")
      return True
    else:
      print(f"gitlab-ci.yml already includes: {scan_build_templates_include} (project ID: {project_id})")
      return False

  except Exception as e:
    print(f"Error updating gitlab-ci.yml for project ID: {project_id} (branch: {branch_name}) - {e}")
    return False

# Replace with your actual values
gitlab_url = "https://gitlab.com"
private_token = os.environ.get("GITLAB_ACCESS_TOKEN")
scan_build_templates_include = "includes: scan_build_templates"

# Get project IDs using a separate script (consider using previous responses)
project_ids = [12345, 67890]  # Replace with your actual project IDs

# Loop through projects and update files
for project_id in project_ids:
  updated = update_gitlab_ci_yml_with_scan_build_templates(gitlab_url, private_token, project_id, "master", scan_build_templates_include)
  if not updated:
    print(f"Project ID: {project_id} might not have a gitlab-ci.yml file or there might be errors retrieving it.")
