import gitlab

# GitLab API URL and access token
GITLAB_URL = 'https://gitlab.example.com'  # Replace with your GitLab instance URL
ACCESS_TOKEN = 'your_access_token_here'  # Replace with your GitLab access token

# Group ID and Project ID for which you want to retrieve the tree information
GROUP_ID = 123  # Replace with your group ID
PROJECT_ID = 456  # Replace with your project ID

def get_project_tree(group_id, project_id):
    # Connect to GitLab instance
    gl = gitlab.Gitlab(GITLAB_URL, private_token=ACCESS_TOKEN)

    try:
        # Get the project by ID
        project = gl.projects.get(project_id, group_id=group_id)

        # Get the tree information for the project
        tree = project.repository_tree()

        return tree
    except gitlab.exceptions.GitlabGetError as e:
        print(f"Error: {e.response_body}")

if __name__ == "__main__":
    project_tree = get_project_tree(GROUP_ID, PROJECT_ID)
    if project_tree:
        print("Tree information for Project ID:", PROJECT_ID)
        for item in project_tree:
            print(item)  # Print or process each item in the tree
    else:
        print("Failed to retrieve tree information for Project ID:", PROJECT_ID)
