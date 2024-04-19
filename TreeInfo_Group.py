import gitlab

# GitLab API URL and access token
GITLAB_URL = 'https://gitlab.example.com'  # Replace with your GitLab instance URL
ACCESS_TOKEN = 'your_access_token_here'  # Replace with your GitLab access token

# Group ID for which you want to retrieve the tree information
GROUP_ID = 123  # Replace with your group ID

def get_group_tree(group_id):
    # Connect to GitLab instance
    gl = gitlab.Gitlab(GITLAB_URL, private_token=ACCESS_TOKEN)

    try:
        # Get the group by ID
        group = gl.groups.get(group_id)

        # Get the tree information for the group
        tree = group.tree(all=True)

        return tree
    except gitlab.exceptions.GitlabGetError as e:
        print(f"Error: {e.response_body}")

if __name__ == "__main__":
    group_tree = get_group_tree(GROUP_ID)
    if group_tree:
        print("Tree information for Group ID:", GROUP_ID)
        for item in group_tree:
            print(item)  # Print or process each item in the tree
    else:
        print("Failed to retrieve tree information for Group ID:", GROUP_ID)
