import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import time
from utils import get_github_repos, create_skills_chart, create_experience_chart

# Page configuration
st.set_page_config(
    page_title="Jadon Telep - Data Science Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add modern styling with custom CSS
st.markdown("""
<style>
    /* Main background and font colors */
    body {
        background-color: #ffffff;
        color: #333333;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Animation for page transitions */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Apply animation to main containers */
    .main .block-container {
        animation: fadeIn 0.5s ease-out;
        background-color: #ffffff;
    }
    
    /* Styled cards */
    .custom-card {
        background-color: #f8f9fa !important;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #333333;
    }
    
    /* Hover effects for buttons and cards */
    .stButton button {
        transition: all 0.3s ease !important;
        background-color: #0066cc !important;
        color: white !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
        background-color: #0055aa !important;
    }
    
    /* Hover effects for cards */
    .experience-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
    }
    
    /* Social buttons */
    .social-button:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }
    
    a:hover {
        opacity: 0.8;
    }
    
    /* Headers styling */
    h1, h2, h3, h4, h5, h6 {
        color: #0066cc;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Paragraph text */
    p, li {
        color: #333333;
        font-family: 'Roboto', sans-serif;
        line-height: 1.6;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        color: #333333;
    }
</style>
""", unsafe_allow_html=True)

# Modern styled sidebar
with st.sidebar:
    # Name and title first, then profile image
    name_color = "#0066cc"
    subtitle_color = "#666666"
    
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
        <h2 style="color:{name_color}; margin-top: 15px; margin-bottom: 10px;">Jadon Telep</h2>
        <p style="color: {subtitle_color}; margin-bottom: 15px;">Computer Science Graduate | Data Scientist</p>
        <img src="./assets/profile_placeholder.svg" width="120">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <h4 style="color:#0066cc; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px;">Navigation</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Modern navigation with custom styling
    page = st.radio("Navigation Menu", ["Home", "Projects", "GitHub", "Contact"], 
                    label_visibility="collapsed")
    
    # Contact info with custom styling
    st.markdown("""
    <div style="margin-top: 30px;">
        <h4 style="color:#0066cc; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px;">Contact</h4>
        <p>📧 jadon.telep@gmail.com</p>
        <p>📱 (602)-541-8579</p>
        <p>📍 Phoenix, Arizona</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Social links with modern styling
    st.markdown("""
    <div style="margin-top: 20px;">
        <h4 style="color:#0066cc; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px;">Social Links</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a row of buttons for social links
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <a href="https://linkedin.com/in/jadontelep" target="_blank" style="text-decoration: none;">
            <div style="background-color:#f8f9fa; padding:8px; text-align:center; border-radius:5px;">
                LinkedIn
            </div>
        </a>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <a href="https://github.com/JadonTelep" target="_blank" style="text-decoration: none;">
            <div style="background-color:#f8f9fa; padding:8px; text-align:center; border-radius:5px;">
                GitHub
            </div>
        </a>
        """, unsafe_allow_html=True)

# Function to create a page transition animation
def page_transition():
    # Add loading animation
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.005)  # Small delay
        progress_bar.progress(percent_complete + 1)
    progress_bar.empty()  # Hide progress bar after completion

# Previous page tracking for animation
if 'previous_page' not in st.session_state:
    st.session_state.previous_page = None

# If page changed, show transition
if st.session_state.previous_page != page:
    page_transition()
    st.session_state.previous_page = page

# Main content
if page == "Home":
    st.title("Data Science Portfolio")
    
    # Modern two-column layout for intro
    intro_col1, intro_col2 = st.columns([3, 2])
    
    with intro_col1:
        st.markdown("""
        ## About Me
        
        Computer science graduate with a Bachelor of Science in Applied Computing and a Minor in Mathematics.
        I have experience developing database and cloud solutions for military intelligence teams and specialize 
        in the use of modern machine learning models in accessibility and learnability.
        
        I'm passionate about creating data-driven solutions that solve real-world problems and improve efficiency.
        """)
    
    with intro_col2:
        # Create an expertise card with modern styling
        card_bg = "#f8f9fa"
        title_color = "#0066cc"
        
        st.markdown(f"""
        <div style="background-color:{card_bg}; padding:15px; border-radius:10px; margin-top:20px;">
        <h3 style="color:{title_color};">Expertise</h3>
        <ul>
          <li>Programming (Python, SQL, R)</li>
          <li>Machine Learning & Deep Learning</li>
          <li>Data Analysis & Statistical Methods</li>
          <li>Natural Language Processing</li>
          <li>Large Language Models</li>
          <li>Database Solutions</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Professional Experience in list format
    st.subheader("Professional Experience")
    
    # Styling
    card_bg = "#f8f9fa"
    title_color = "#0066cc"
    
    st.markdown(f"""
    <div class="experience-card" style="background-color:{card_bg}; padding:20px; border-radius:10px; margin-bottom:20px; transition: transform 0.3s ease, box-shadow 0.3s ease;">
        <h4 style="color:{title_color};">Data Scientist - DOD 501st Military Intelligence Brigade</h4>
        <p><strong>Period:</strong> 01/2023 - 05/2023</p>
        <ul>
            <li>Worked directly with DoD personnel crafting and refining solutions for ongoing computerbased issues.</li>
            <li>Designed cloud based solution for Korean allied forces intelligence teams.</li>
            <li>Created image recognition program for labeling images of military equipment.</li>
        </ul>
    </div>
    
    <div class="experience-card" style="background-color:{card_bg}; padding:20px; border-radius:10px; margin-bottom:20px; transition: transform 0.3s ease, box-shadow 0.3s ease;">
        <h4 style="color:{title_color};">Network Security Intern - CSAA Insurance</h4>
        <p><strong>Period:</strong> 01/2024 - 05/2024</p>
        <ul>
            <li>Implemented comprehensive network monitoring systems to protect sensitive data</li>
            <li>Configured VPN management systems for secure remote access for employees</li>
            <li>Reduced unauthorized access attempts through security enhancement measures</li>
        </ul>
    </div>
    
    <div class="experience-card" style="background-color:{card_bg}; padding:20px; border-radius:10px; margin-bottom:20px; transition: transform 0.3s ease, box-shadow 0.3s ease;">
        <h4 style="color:{title_color};">IT Service Technician - CSAA Insurance</h4>
        <p><strong>Period:</strong> 05/2022 - Present</p>
        <ul>
            <li>Resolved network, access, and end user equipment issues</li>
            <li>Established tickets for engaging support through established ticketing system</li>
            <li>Worked with local and international contractors to establish access to virtual desktops.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Education with modern styling 
    st.subheader("Education")
    
    edu_col1, edu_col2 = st.columns([3, 1])
    with edu_col1:
        st.markdown("""
        #### Bachelor of Science in Applied Computing
        **Arizona State University** | Graduation: December 2024
        """)
    with edu_col2:
        st.markdown("**GPA: 3.4**")
        st.markdown("*Cum Laude*")
    
    st.markdown("**Minor in Mathematics** - Arizona State University")

elif page == "Projects":
    st.title("Data Science Projects")
    
    # Project 1
    st.header("Project 1: Military Equipment Image Recognition")
    
    st.markdown("""
    ### Overview
    Developed an image recognition program for the DOD 501st Military Intelligence Brigade to identify and 
    label images of tanks, motorized vehicles, and other military equipment submitted by civilians in 
    Ukraine and Korea.
    
    ### Technologies Used
    * Python (TensorFlow, Keras)
    * YOLO Computer Vision
    
    ### Results
    Created a robust classification system with over 95% accuracy in identifying critical military equipment, 
    significantly enhancing intelligence capabilities for allied forces.
    """)
    
    #st.markdown("[View GitHub Repository](https://github.com/JadonTelep/)")
    
    # Project 2
    st.header("Project 2: Military Intelligence Database Solutions")
    
    st.markdown("""
    ### Overview
    Developed a comprehensive database solution for the DOD 501st Military Intelligence Brigade to streamline 
    intelligence reporting and data analysis. The system enabled secure storage, retrieval, and analysis of 
    critical intelligence data across multiple security classifications.
    
    ### Technologies Used
    * SQL and Database Design
    * Data Modeling and Normalization
    * Secure Authentication Systems
    * Cloud Integration
    * Data Migration and ETL Processes
    
    ### Results
    Improved intelligence data retrieval speed and reduced reporting time, significantly 
    enhancing operational effectiveness for field units while maintaining robust security protocols.
    """)
    
    #st.markdown("[View GitHub Repository](https://github.com/JadonTelep/)")
    
    # Project 3
    st.header("Project 3: Network Security and VPN Management System")
    
    st.markdown("""
    ### Overview
    Reviewed and revised a comprehensive network security monitoring system during my internship at CSAA. 
    The system included VPN management, firewall configuration, and real-time security alert monitoring to 
    protect sensitive company data and ensure network integrity.
    
    ### Technologies Used
    * Network Security Protocols
    * Firewall Configuration and Management
    * VPN Administration
    * Security Monitoring Tools
    
    ### Results
    Enhanced overall network security posture, reduced unauthorized access attempts, 
    and streamlined VPN access management for remote employees, improving both security and productivity.
    """)
    
    #st.markdown("[View GitHub Repository](https://github.com/JadonTelep/)")

elif page == "GitHub":
    st.title("GitHub Repositories")
    
    # Hardcoded GitHub username
    github_username = "jadontelep"
    
    with st.spinner(f"Fetching repositories for {github_username}..."):
        try:
            repos = get_github_repos(github_username)
            
            if repos:
                st.success(f"Found {len(repos)} public repositories")
                
                # Create selectable repo list
                repo_names = [repo["name"] for repo in repos]
                selected_repo = st.selectbox("Select a repository to view details", repo_names)
                
                # Find the selected repo
                selected_repo_data = next((repo for repo in repos if repo["name"] == selected_repo), None)
                
                if selected_repo_data:
                    st.subheader(selected_repo_data["name"])
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Description**: {selected_repo_data['description'] or 'No description available'}")
                        st.markdown(f"**Language**: {selected_repo_data['language'] or 'Not specified'}")
                        st.markdown(f"**Created**: {selected_repo_data['created_at'].split('T')[0]}")
                        st.markdown(f"**Last Updated**: {selected_repo_data['updated_at'].split('T')[0]}")
                        st.markdown(f"**URL**: [{selected_repo_data['html_url']}]({selected_repo_data['html_url']})")
                    
                    with col2:
                        st.metric("Stars", selected_repo_data["stargazers_count"])
                        st.metric("Forks", selected_repo_data["forks_count"])
                        st.metric("Watchers", selected_repo_data["watchers_count"])
                        st.metric("Open Issues", selected_repo_data["open_issues_count"])
                
                # Display repositories in a table with a slider to control how many to show
                st.subheader("Repositories")
                
                # Create DataFrame with repos
                repo_data = []
                for repo in repos:
                    repo_data.append({
                        "Name": repo["name"],
                        "Language": repo["language"] or "Not specified",
                        "Stars": repo["stargazers_count"],
                        "Forks": repo["forks_count"],
                        "Last Updated": repo["updated_at"].split("T")[0],
                        "URL": repo["html_url"]
                    })
                
                repo_df = pd.DataFrame(repo_data)
                
                # Sort by update date (most recent first)
                repo_df['Last Updated'] = pd.to_datetime(repo_df['Last Updated'])
                repo_df = repo_df.sort_values(by='Last Updated', ascending=False)
                repo_df['Last Updated'] = repo_df['Last Updated'].dt.strftime('%Y-%m-%d')
                
                # Create clickable links
                def make_clickable(url, name):
                    return f'<a href="{url}" target="_blank">{name}</a>'
                
                repo_df['Name'] = repo_df.apply(lambda x: make_clickable(x['URL'], x['Name']), axis=1)
                repo_df = repo_df.drop(columns=['URL'])
                
                # Always show only the 5 most recent repositories
                st.write("Showing the 5 most recent repositories:")
                
                # Display the 5 most recent repositories
                st.write(repo_df.head(5).to_html(escape=False, index=False), unsafe_allow_html=True)
                
            else:
                st.warning(f"No public repositories found for {github_username}")
        
        except Exception as e:
            st.error(f"Error fetching GitHub repositories: {str(e)}")


elif page == "Contact":
    st.title("Contact Me")
    
    # Get current theme colors
    card_bg = "#f8f9fa"
    title_color = "#0066cc"
    
    st.markdown(f"""
    <div style="background-color:{card_bg}; padding:20px; border-radius:10px; margin-bottom:30px; 
         animation: fadeIn 0.5s ease-out;">
        <p style="font-size:18px;">
        I'm always open to discussing data science projects, job opportunities, or collaborations.
        Feel free to reach out to me through any of the following methods:
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact form with modern styling
    title_color = "#0066cc"
    
    st.markdown(f"""
    <h3 style="color:{title_color}; margin-bottom:20px; animation: fadeIn 0.6s ease-out;">Send Me a Message</h3>
    """, unsafe_allow_html=True)
    
    # Contact form with animation delay
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message", height=150)
        
        # Add some animations to the button
        st.markdown("""
        <style>
        .stButton button {
            transition: all 0.3s ease !important;
        }
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        submitted = st.form_submit_button("Send Message")
        
        if submitted:
            if name and email and message:
                st.success("Thank you for reaching out! I'll get back to you as soon as possible.")
                # In a real application, you would add code here to send the message
            else:
                st.error("Please fill in all required fields.")
    
    # Availability section with card styling
    card_bg = "#e8f4f8" 
    title_color = "#0066cc"
    
    st.markdown(f"""
    <div style="background-color:{card_bg}; padding:20px; border-radius:10px; margin-top:30px; animation: fadeIn 0.7s ease-out;
         box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s ease, box-shadow 0.3s ease;">
        <h3 style="color:{title_color}; margin-bottom:15px;">Availability</h3>
        <p style="font-size:16px;">I'm currently available for freelance work, consulting, and full-time positions. My typical response time is within 24-48 hours.</p>
    </div>
    """, unsafe_allow_html=True)