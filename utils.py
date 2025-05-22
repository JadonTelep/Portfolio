import requests
import os
import streamlit as st

def get_github_repos(username):
    """
    Fetch GitHub repositories for a specific user
    """
    url = f"https://api.github.com/users/{username}/repos"
    
    # Check if a GitHub token is available in environment variables
    github_token = os.getenv("GITHUB_TOKEN", "")
    
    if github_token:
        headers = {"Authorization": f"token {github_token}"}
    else:
        headers = {}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        repos = response.json()
        # Sort repos by stars in descending order
        repos.sort(key=lambda x: x.get("stargazers_count", 0), reverse=True)
        
        return repos
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching GitHub repositories: {str(e)}")
        return []