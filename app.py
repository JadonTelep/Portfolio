import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import requests
import time
from utils import get_github_repos, create_skills_chart, create_experience_chart

# Page configuration
st.set_page_config(
    page_title="Data Science Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for animations and global styling
st.markdown("""
<style>
    /* Animation for page transitions */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Apply animation to main containers */
    .main .block-container {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Hover effects for buttons and cards */
    div[data-testid="stHorizontalBlock"] > div:hover {
        transform: translateY(-3px);
        transition: transform 0.3s ease;
    }
    
    /* Style adjustments for dark mode compatibility */
    .stButton button:hover {
        border-color: rgb(0, 102, 204) !important;
    }
    
    /* Card styling with hover effects */
    div[data-testid="stVerticalBlock"] div[style*="background-color:#f8f9fa"] {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    div[data-testid="stVerticalBlock"] div[style*="background-color:#f8f9fa"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* Position the dark mode toggle at the top right */
    .dark-mode-container {
        position: fixed;
        top: 0;
        right: 0;
        padding: 10px 20px;
        z-index: 1000;
        display: flex;
        align-items: center;
        background-color: rgba(0, 0, 0, 0.05);
        border-radius: 0 0 0 10px;
    }
    
    /* Make all text respect dark mode */
    .dark-mode-active {
        background-color: #121212 !important;
        color: #ffffff !important;
    }
    
    .dark-mode-active p, .dark-mode-active span, .dark-mode-active h1, 
    .dark-mode-active h2, .dark-mode-active h3, .dark-mode-active h4, 
    .dark-mode-active h5, .dark-mode-active h6, .dark-mode-active li {
        color: #e0e0e0 !important;
    }
    
    /* Dark mode card styling */
    .dark-mode-card {
        background-color: #1e1e1e !important;
        border: 1px solid #333333;
    }
</style>
""", unsafe_allow_html=True)

# Add modern styling with custom CSS
st.markdown("""
<style>
    /* Animation for page transitions */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Apply animation to main containers */
    .main .block-container {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Styled cards */
    .custom-card {
        background-color: #f8f9fa !important;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Hover effects for buttons and cards */
    .stButton button {
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }
    
    a:hover {
        opacity: 0.8;
    }
</style>
""")

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
        <a href="https://github.com/jadontelep" target="_blank" style="text-decoration: none;">
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
        # Create an expertise card with modern styling that respects dark mode
        card_bg = "#1e1e1e" if st.session_state.dark_mode else "#f8f9fa"
        title_color = "#4d94ff" if st.session_state.dark_mode else "#0066cc"
        
        st.markdown(f"""
        <div style="background-color:{card_bg}; padding:15px; border-radius:10px; margin-top:20px;">
        <h3 style="color:{title_color};">Expertise</h3>
        <ul class="dark-mode-text">
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
    
    # Dark mode compatible styling
    card_bg = "#1e1e1e" if st.session_state.dark_mode else "#f8f9fa"
    title_color = "#4d94ff" if st.session_state.dark_mode else "#0066cc"
    
    st.markdown(f"""
    <div class="experience-card" style="background-color:{card_bg}; padding:20px; border-radius:10px; margin-bottom:20px; transition: transform 0.3s ease, box-shadow 0.3s ease;">
        <h4 style="color:{title_color};">Data Scientist - DOD 501st Military Intelligence Brigade</h4>
        <p class="dark-mode-text"><strong>Period:</strong> 2022 - 2024</p>
        <ul class="dark-mode-text">
            <li>Developed machine learning models to identify military equipment from images with 90% accuracy</li>
            <li>Designed intelligence database solutions that improved data retrieval speed by 65%</li>
            <li>Created analysis tools for field intelligence processing, reducing reporting time by 40%</li>
        </ul>
    </div>
    
    <div class="experience-card" style="background-color:{card_bg}; padding:20px; border-radius:10px; margin-bottom:20px; transition: transform 0.3s ease, box-shadow 0.3s ease;">
        <h4 style="color:{title_color};">Network Security Intern - CSAA Insurance</h4>
        <p class="dark-mode-text"><strong>Period:</strong> 2021 - 2022</p>
        <ul class="dark-mode-text">
            <li>Implemented comprehensive network monitoring systems to protect sensitive data</li>
            <li>Configured VPN management systems for secure remote access for employees</li>
            <li>Reduced unauthorized access attempts by 78% through security enhancement measures</li>
        </ul>
    </div>
    
    <div class="experience-card" style="background-color:{card_bg}; padding:20px; border-radius:10px; margin-bottom:20px; transition: transform 0.3s ease, box-shadow 0.3s ease;">
        <h4 style="color:{title_color};">Research Assistant - Arizona State University</h4>
        <p class="dark-mode-text"><strong>Period:</strong> 2020 - 2021</p>
        <ul class="dark-mode-text">
            <li>Assisted faculty with research on accessibility in machine learning models</li>
            <li>Conducted statistical analysis of model performance across diverse user groups</li>
            <li>Contributed to two published papers on learnability in AI systems</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Add JavaScript for experience card hover effects
    st.markdown("""
    <style>
    .experience-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
    }
    </style>
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
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Overview
        Developed an image recognition program for the DOD 501st Military Intelligence Brigade to identify and 
        label images of tanks, motorized vehicles, and other military equipment submitted by civilians in 
        Ukraine and Korea.
        
        ### Technologies Used
        * Python (TensorFlow, Keras)
        * Convolutional Neural Networks
        * Computer Vision
        * Transfer Learning (MobileNet)
        
        ### Results
        Created a robust classification system with over 90% accuracy in identifying critical military equipment, 
        significantly enhancing intelligence capabilities for allied forces.
        """)
    
    with col2:
        # Create a visualization representing the image classification results
        fig, ax = plt.subplots(figsize=(5, 4))
        
        # Sample data for classification accuracy
        equipment_types = ['Tanks', 'APCs', 'Artillery', 'Aircraft', 'Other']
        accuracy = [94, 91, 88, 85, 81]
        
        # Create bar chart for classification accuracy
        bars = ax.bar(equipment_types, accuracy, color='skyblue')
        
        # Add a horizontal line for target accuracy
        ax.axhline(y=85, linestyle='--', color='red', alpha=0.7, label='Target Accuracy')
        
        # Add labels and title
        ax.set_ylim([75, 100])
        ax.set_title('Military Equipment Classification Accuracy')
        ax.set_xlabel('Equipment Type')
        ax.set_ylabel('Accuracy (%)')
        ax.grid(axis='y', alpha=0.3)
        ax.legend()
        
        # Add data labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height}%', ha='center', va='bottom')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    
    st.markdown("[View GitHub Repository](https://github.com/jadontelep/military-equipment-recognition)")
    
    # Project 2
    st.header("Project 2: Military Intelligence Database Solutions")
    col1, col2 = st.columns([2, 1])
    
    with col1:
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
        Improved intelligence data retrieval speed by 65% and reduced reporting time by 40%, significantly 
        enhancing operational effectiveness for field units while maintaining robust security protocols.
        """)
    
    with col2:
        # Create a visualization for database performance improvements
        fig, ax = plt.subplots(figsize=(5, 4))
        
        # Sample data for before/after comparison
        metrics = ['Query Time', 'Report Gen', 'Data Entry', 'Analysis']
        before = [65, 45, 30, 85]  # Times in seconds before optimization
        after = [22, 27, 12, 32]   # Times in seconds after optimization
        
        x = np.arange(len(metrics))  # the label locations
        width = 0.35  # the width of the bars
        
        ax.bar(x - width/2, before, width, label='Before', color='#ff9999')
        ax.bar(x + width/2, after, width, label='After', color='#66b3ff')
        
        # Add labels and title
        ax.set_title('Database Performance Improvements')
        ax.set_ylabel('Time (seconds)')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.legend()
        
        # Add percentage improvement labels
        for i, (b, a) in enumerate(zip(before, after)):
            improvement = ((b - a) / b) * 100
            ax.text(i, max(b, a) + 5, f"-{improvement:.0f}%", ha='center')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    st.markdown("[View GitHub Repository](https://github.com/jadontelep/military-intelligence-db)")
    
    # Project 3
    st.header("Project 3: Network Security and VPN Management System")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Overview
        Designed and implemented a comprehensive network security monitoring system during my internship at CSAA. 
        The system included VPN management, firewall configuration, and real-time security alert monitoring to 
        protect sensitive company data and ensure network integrity.
        
        ### Technologies Used
        * Network Security Protocols
        * Firewall Configuration and Management
        * VPN Administration
        * Python for Log Analysis
        * Security Monitoring Tools
        
        ### Results
        Enhanced overall network security posture, reduced unauthorized access attempts by 78%, 
        and streamlined VPN access management for remote employees, improving both security and productivity.
        """)
    
    with col2:
        # Create a security incidents visualization
        categories = ['Authentication Failures', 'Unauthorized Access', 'Suspicious Traffic', 'Policy Violations', 'Misconfiguration']
        before_counts = [156, 89, 123, 72, 47]
        after_counts = [34, 21, 87, 45, 12]
        
        # Create a comparison bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=categories,
            y=before_counts,
            name='Before Implementation',
            marker_color='indianred'
        ))
        
        fig.add_trace(go.Bar(
            x=categories,
            y=after_counts,
            name='After Implementation',
            marker_color='royalblue'
        ))
        
        fig.update_layout(
            title='Security Incidents Reduction',
            xaxis_tickangle=-45,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            ),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("[View GitHub Repository](https://github.com/jadontelep/network-security-tools)")

elif page == "Skills":
    st.title("Technical Skills")
    
    # Skills categories
    skills_categories = {
        "Programming Languages": {
            "Python": 95,
            "R": 85,
            "SQL": 90,
            "SAS": 80
        },
        "Data Science & ML": {
            "Machine Learning": 90,
            "Statistical Analysis": 88,
            "Deep Learning": 85,
            "Natural Language Processing": 82,
            "Large Language Models": 80
        },
        "Data Processing": {
            "Data Cleaning": 92,
            "Data Wrangling": 90,
            "Data Analytics": 88
        },
        "IT & Networking": {
            "Network Troubleshooting": 85,
            "Cybersecurity": 80,
            "Firewall Configuration": 78,
            "VPN Management": 82
        }
    }
    
    # Display interactive skills charts
    for category, skills in skills_categories.items():
        st.subheader(category)
        fig = create_skills_chart(skills)
        st.plotly_chart(fig, use_container_width=True)
    
    # Projects by technology
    st.subheader("Projects by Technology")
    
    # Sample data for visualization
    techs = [
        "Python", "Machine Learning", "Deep Learning", 
        "NLP", "Computer Vision", "Time Series", 
        "Data Visualization", "Statistical Analysis"
    ]
    counts = [12, 8, 5, 4, 3, 6, 9, 7]
    
    fig = px.bar(
        x=techs, 
        y=counts,
        labels={'x': 'Technology', 'y': 'Number of Projects'},
        title='Projects by Technology',
        color=counts,
        color_continuous_scale='viridis'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

elif page == "GitHub":
    st.title("GitHub Repositories")
    
    # GitHub username input
    github_username = st.text_input("GitHub Username", "jadontelep")
    
    if github_username:
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
                    
                    # Display all repositories in a table
                    st.subheader("All Repositories")
                    
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
                    
                    # Create clickable links
                    def make_clickable(url, name):
                        return f'<a href="{url}" target="_blank">{name}</a>'
                    
                    repo_df['Name'] = repo_df.apply(lambda x: make_clickable(x['URL'], x['Name']), axis=1)
                    repo_df = repo_df.drop(columns=['URL'])
                    
                    st.write(repo_df.to_html(escape=False, index=False), unsafe_allow_html=True)
                    
                else:
                    st.warning(f"No public repositories found for {github_username}")
            
            except Exception as e:
                st.error(f"Error fetching GitHub repositories: {str(e)}")

elif page == "Contact":
    st.title("Contact Me")
    
    # Get current theme colors
    card_bg = "#1e1e1e" if st.session_state.dark_mode else "#f8f9fa"
    text_color_class = "dark-mode-text"
    
    st.markdown(f"""
    <div style="background-color:{card_bg}; padding:20px; border-radius:10px; margin-bottom:30px; 
         animation: fadeIn 0.5s ease-out;">
        <p class="{text_color_class}" style="font-size:18px;">
        I'm always open to discussing data science projects, job opportunities, or collaborations.
        Feel free to reach out to me through any of the following methods:
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Modern two-column layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Contact information card with dark mode support
        card_bg = "#1e1e1e" if st.session_state.dark_mode else "#f8f9fa"
        title_color = "#4d94ff" if st.session_state.dark_mode else "#0066cc"
        border_color = "#444444" if st.session_state.dark_mode else "#eeeeee"
        btn_bg = "#2d2d2d" if st.session_state.dark_mode else "#ffffff"
        btn_border = "#555555" if st.session_state.dark_mode else "#dddddd"
        
        st.markdown(f"""
        <div style="background-color:{card_bg}; padding:20px; border-radius:10px; height:100%; animation: fadeIn 0.5s ease-out;">
            <h3 style="color:{title_color}; margin-bottom:20px; border-bottom:1px solid {border_color}; padding-bottom:10px;">Contact Information</h3>
            
            <div style="margin-bottom:15px;">
                <p class="dark-mode-text" style="font-weight:bold; margin-bottom:5px;">Email</p>
                <p class="dark-mode-text" style="margin-left:10px;">📧 jadon.telep@gmail.com</p>
            </div>
            
            <div style="margin-bottom:15px;">
                <p class="dark-mode-text" style="font-weight:bold; margin-bottom:5px;">Phone</p>
                <p class="dark-mode-text" style="margin-left:10px;">📱 (602)-541-8579</p>
            </div>
            
            <div style="margin-bottom:25px;">
                <p class="dark-mode-text" style="font-weight:bold; margin-bottom:5px;">Location</p>
                <p class="dark-mode-text" style="margin-left:10px;">📍 Phoenix, Arizona</p>
            </div>
            
            <h4 style="color:{title_color}; margin-top:30px; margin-bottom:15px; border-bottom:1px solid {border_color}; padding-bottom:10px;">Social Media</h4>
            
            <div style="display:flex; gap:10px; flex-wrap:wrap;">
                <a href="https://linkedin.com/in/jadontelep" target="_blank" style="text-decoration:none;">
                    <div class="social-button" style="background-color:{btn_bg}; padding:8px 15px; border-radius:5px; border:1px solid {btn_border}; transition: transform 0.2s ease, box-shadow 0.2s ease;">
                        <span class="dark-mode-text">LinkedIn</span>
                    </div>
                </a>
                <a href="https://github.com/jadontelep" target="_blank" style="text-decoration:none;">
                    <div class="social-button" style="background-color:{btn_bg}; padding:8px 15px; border-radius:5px; border:1px solid {btn_border}; transition: transform 0.2s ease, box-shadow 0.2s ease;">
                        <span class="dark-mode-text">GitHub</span>
                    </div>
                </a>
            </div>
            
            <style>
            .social-button:hover {
                box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
            }
            </style>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Contact form with modern styling and dark mode support
        title_color = "#4d94ff" if st.session_state.dark_mode else "#0066cc"
        
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
    
    # Availability section with card styling and dark mode support
    card_bg = "#1e2c3a" if st.session_state.dark_mode else "#e8f4f8" 
    title_color = "#4d94ff" if st.session_state.dark_mode else "#0066cc"
    
    st.markdown(f"""
    <div style="background-color:{card_bg}; padding:20px; border-radius:10px; margin-top:30px; animation: fadeIn 0.7s ease-out;
         box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s ease, box-shadow 0.3s ease;">
        <h3 style="color:{title_color}; margin-bottom:15px;">Availability</h3>
        <p class="dark-mode-text" style="font-size:16px;">I'm currently available for freelance work, consulting, and full-time positions. My typical response time is within 24-48 hours.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add some JavaScript for hover effects that are React-friendly
    st.markdown("""
    <script>
    // Add hover effects using JavaScript event listeners
    document.addEventListener('DOMContentLoaded', function() {
        const cards = document.querySelectorAll('div[style*="border-radius:10px"]');
        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px)';
                this.style.boxShadow = '0 10px 20px rgba(0,0,0,0.2)';
            });
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)
