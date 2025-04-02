import requests
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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

def create_skills_chart(skills):
    """
    Create a horizontal bar chart showing skills and proficiency levels
    """
    skills_df = pd.DataFrame({
        'Skill': list(skills.keys()),
        'Proficiency': list(skills.values())
    })
    
    # Sort by proficiency
    skills_df = skills_df.sort_values('Proficiency', ascending=True)
    
    fig = go.Figure(go.Bar(
        x=skills_df['Proficiency'],
        y=skills_df['Skill'],
        orientation='h',
        marker=dict(
            color=skills_df['Proficiency'],
            colorscale='viridis',
            colorbar=dict(title='Proficiency'),
        )
    ))
    
    fig.update_layout(
        xaxis=dict(
            title='Proficiency',
            range=[0, 100]
        ),
        yaxis=dict(
            title=None,
            autorange="reversed"
        ),
        height=300,
        margin=dict(l=0, r=0, t=20, b=0)
    )
    
    return fig

def create_experience_chart():
    """
    Create a timeline chart for professional experience
    """
    experience = [
        dict(Task="DB Engineer - DOD 501st MI Brigade", Start='2023-01-01', Finish='2023-05-01', Resource='Job'),
        dict(Task="Network/Security Intern - CSAA", Start='2024-01-01', Finish='2024-05-01', Resource='Internship'),
        dict(Task="IT Service Tech - CSAA IG", Start='2022-05-01', Finish='2025-04-02', Resource='Job'),
    ]
    
    df = pd.DataFrame(experience)
    
    fig = px.timeline(
        df, 
        x_start="Start", 
        x_end="Finish", 
        y="Task",
        color="Resource",
        color_discrete_map={
            "Job": "blue",
            "Internship": "green",
            "Project": "orange"
        },
        labels={"Task": "Position"}
    )
    
    fig.update_layout(
        xaxis=dict(
            title=None,
            type='date',
            tickformat='%b %Y'
        ),
        yaxis=dict(
            title=None,
            autorange="reversed"
        ),
        height=300,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    return fig
