# Portfolio Website Deployment Instructions

## Files You Need to Download

1. `app.py` - Main application file (you may want to rename this to `app.py` after downloading)
2. `utils.py` - Utility functions file
3. `.streamlit/config.toml` - Streamlit configuration file
4. All assets in the `assets` folder (if any are used)

## Dependencies

Make sure you have the following Python packages installed:

```
streamlit==1.27.0
pandas==2.0.3
requests==2.31.0
python-dotenv==1.1.0
```

You can install these packages using:

```
pip install -r dependencies.txt
```

## Local Deployment

To run the application locally:

1. Create a folder for your portfolio website
2. Place all the downloaded files in the folder, maintaining the same structure
3. Create a `.streamlit` folder and place the `config.toml` file inside it
4. Open a terminal/command prompt in the folder
5. Run: `streamlit run app_new.py` (or `app.py` if you renamed it)

## Cloud Deployment Options

### Streamlit Cloud (Recommended)

1. Create a GitHub repository and push all your files to it
2. Sign up for an account at [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository to Streamlit Cloud
4. Deploy your app with a few clicks

### Heroku

1. Create a `requirements.txt` file with the dependencies listed above
2. Create a `Procfile` with the content: `web: streamlit run app_new.py --server.port $PORT`
3. Push your code to a GitHub repository
4. Deploy to Heroku from the GitHub repository

### Railway, Render, or other PaaS

Most Platform as a Service providers have similar deployment processes:

1. Connect to your GitHub repository
2. Set the build command to install the dependencies
3. Set the start command to run your Streamlit app

## Important Notes

- Make sure your GitHub username is correctly set in the application (currently set to "jadontelep")
- The portfolio is configured to work with light mode theme
- The server settings in `config.toml` should be maintained for proper deployment
