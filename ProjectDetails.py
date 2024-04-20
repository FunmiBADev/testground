import gitlab
import gitlab.exceptions

# https://gitlab.com/FunmiBADev/DevOps-Course-Starter

token = "TBD"

access_token = "TBD"

# Connect to GitLab instance
gl = gitlab.Gitlab("https://gitlab.com", private_token=token)

def get_project_by_name(project_name, token):

  try:
    # Search for project by name
    projects = gl.projects.list(search=project_name)

    # Assuming there's only one project with the given name
    if projects:
      return projects[0]
    else:
      print(f"No project found with the name '{project_name}'")
      return None
  except gitlab.exceptions.GitlabAuthenticationError:
    print("Failed to authenticate. Please check your GitLab access token.")
    return None
  except gitlab.exceptions.GitlabGetError:
    print(f"Failed to get project '{project_name}'.")
    return None


# Example usage
if __name__ == "__main__":
  project_name = "DevOps-Course-Workshop-Module-07-Learners"
  access_token = "your_access_token_here"

  project_details = get_project_by_name(project_name, access_token)
  if project_details:
    print("Project details:")
    print(project_details)
