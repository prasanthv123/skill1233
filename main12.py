

# Function to create a GitHub repository
def create_github_repo(repo_name):
    repo_data = {
        "name": repo_name,
        "private": False  # Change to True if you want a private repo
    }
    
    response = requests.post(
        GITHUB_URL,
        json=repo_data,
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )
    
    return response

# Function to delete a GitHub repository
def delete_github_repo(repo_name):
    response = requests.delete(
        f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}",
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )
    return response

# Function to list repositories
def list_repositories():
    response = requests.get(
        GITHUB_URL,
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )
    if response.status_code == 200:
        return [repo['name'] for repo in response.json()]
    else:
        st.error(f"Error listing repositories: {response.status_code} - {response.json().get('message')}")
        return []

# Streamlit application
st.title("GitHub Repository Manager")

# Expander for Create/Delete options
with st.expander("Manage Repositories", expanded=True):
    # Select action: Create or Delete Repository
    action = st.selectbox("Select Action:", ("Create Repository", "Delete Repository", "List Repositories"))

    if action == "Create Repository":
        repo_name = st.text_input("Enter the repository name to create:")
        if st.button("Create"):
            if repo_name:
                response = create_github_repo(repo_name)
                if response.status_code == 201:
                    st.success(f"Repository '{repo_name}' created successfully!")
                else:
                    st.error(f"Error creating repository: {response.status_code} - {response.json().get('message')}")
            else:
                st.warning("Please enter a repository name.")

    elif action == "Delete Repository":
        existing_repos = list_repositories()
        if existing_repos:  # Only show the select box if there are repositories
            selected_repo = st.selectbox("Select a repository to delete:", existing_repos)
            if st.button("Delete"):
                if selected_repo:
                    response = delete_github_repo(selected_repo)
                    if response.status_code == 204:
                        st.success(f"Repository '{selected_repo}' deleted successfully!")
                    else:
                        st.error(f"Error deleting repository: {response.status_code} - {response.json().get('message')}")
                else:
                    st.warning("Please select a repository to delete.")
        else:
            st.warning("No repositories available to delete.")

    elif action == "List Repositories":
        if st.button("Show Repositories"):
            existing_repos = list_repositories()
            if existing_repos:
                st.write("Here are your repositories:")
                for repo in existing_repos:
                    st.write(f"- {repo}")
            else:
                st.write("No repositories available.")
