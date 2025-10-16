"""
Authentication Module
====================
This module handles user authentication for the Smart Gold Trading Dashboard.
Uses streamlit-authenticator for secure login/signup functionality.

Functions:
    - initialize_auth: Initialize authentication system
    - login_user: Handle user login
    - signup_user: Handle user registration
    - logout_user: Handle user logout
"""

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
from pathlib import Path


def get_config_path():
    """Get path to authentication config file."""
    return Path(__file__).parent / 'config.yaml'


def create_default_config():
    """Create default authentication configuration."""
    config = {
        'credentials': {
            'usernames': {
                'demo': {
                    'email': 'demo@goldtrading.com',
                    'name': 'Demo User',
                    'password': '$2b$12$KIXl.Huq2vDjvLsEYiB4Ee4QZLkdVJsVCWJwJVXQWvNxwvJjGKX6W'  # hashed 'demo123'
                }
            }
        },
        'cookie': {
            'expiry_days': 30,
            'key': 'smart_gold_trading_key',
            'name': 'smart_gold_trading_cookie'
        },
        'preauthorized': {
            'emails': []
        }
    }
    
    config_path = get_config_path()
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
    
    return config


def load_config():
    """Load authentication configuration."""
    config_path = get_config_path()
    
    if not config_path.exists():
        return create_default_config()
    
    try:
        with open(config_path) as file:
            config = yaml.load(file, Loader=SafeLoader)
        return config
    except Exception as e:
        st.error(f"Error loading config: {str(e)}")
        return create_default_config()


def save_config(config):
    """Save authentication configuration."""
    config_path = get_config_path()
    try:
        with open(config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        return True
    except Exception as e:
        st.error(f"Error saving config: {str(e)}")
        return False


def initialize_auth():
    """
    Initialize authentication system.
    
    Returns:
    --------
    streamlit_authenticator.Authenticate
        Authenticator object
    """
    try:
        config = load_config()
        
        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized']
        )
        
        return authenticator, config
        
    except Exception as e:
        st.error(f"Error initializing authentication: {str(e)}")
        return None, None


def display_login_page():
    """
    Display login/signup page with custom styling.
    
    Returns:
    --------
    tuple
        (authentication_status, username, name)
    """
    # Custom CSS for login page
    st.markdown("""
    <style>
        .login-container {
            max-width: 500px;
            margin: 50px auto;
            padding: 30px;
            background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
            border-radius: 15px;
            border: 2px solid #FFD700;
        }
        .login-title {
            color: #FFD700;
            text-align: center;
            font-size: 32px;
            margin-bottom: 30px;
        }
        .demo-info {
            background-color: #2d2d2d;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            border-left: 4px solid #FFD700;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Center logo and title
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="login-title">
            🏆 Smart Gold Trading Dashboard
        </div>
        """, unsafe_allow_html=True)
    
    # Initialize authenticator
    authenticator, config = initialize_auth()
    
    if authenticator is None:
        st.error("Failed to initialize authentication system.")
        return None, None, None
    
    # Login form
    name, authentication_status, username = authenticator.login('Login', 'main_login')
    
    if authentication_status:
        return authentication_status, username, name
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
    
    # Demo credentials info
    st.markdown("""
    <div class="demo-info">
        <h4 style="color: #FFD700; margin-top: 0;">🎯 Demo Credentials</h4>
        <p style="color: #cccccc; margin: 5px 0;">
            <strong>Username:</strong> demo<br>
            <strong>Password:</strong> demo123
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Signup option
    st.markdown("---")
    with st.expander("📝 Create New Account"):
        signup_form(config)
    
    return authentication_status, username, name


def signup_form(config):
    """
    Display signup form for new users.
    
    Parameters:
    -----------
    config : dict
        Authentication configuration
    """
    st.subheader("Register New User")
    
    with st.form("signup_form_auth"):
        new_username = st.text_input("Username")
        new_name = st.text_input("Full Name")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submitted = st.form_submit_button("Create Account")
        
        if submitted:
            # Validation
            if not all([new_username, new_name, new_email, new_password, confirm_password]):
                st.error("All fields are required!")
                return
            
            if new_password != confirm_password:
                st.error("Passwords do not match!")
                return
            
            if new_username in config['credentials']['usernames']:
                st.error("Username already exists!")
                return
            
            # Hash password
            hashed_password = stauth.Hasher([new_password]).generate()[0]
            
            # Add new user to config
            config['credentials']['usernames'][new_username] = {
                'email': new_email,
                'name': new_name,
                'password': hashed_password
            }
            
            # Save config
            if save_config(config):
                st.success("Account created successfully! Please login with your credentials.")
            else:
                st.error("Failed to create account. Please try again.")


def display_logout_button(authenticator, name):
    """
    Display logout button in sidebar.
    
    Parameters:
    -----------
    authenticator : streamlit_authenticator.Authenticate
        Authenticator object
    name : str
        User's name
    """
    with st.sidebar:
        st.markdown(f"""
        <div style="
            background-color: #2d2d2d;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #FFD700;
        ">
            <p style="color: #FFD700; margin: 0; font-size: 14px;">Logged in as:</p>
            <p style="color: white; margin: 5px 0 0 0; font-size: 18px; font-weight: bold;">{name}</p>
        </div>
        """, unsafe_allow_html=True)
        
        authenticator.logout('Logout', 'sidebar_logout')


def check_authentication():
    """
    Check if user is authenticated and display login page if not.
    
    Returns:
    --------
    tuple
        (is_authenticated, username, name, authenticator)
    """
    # Initialize session state for authentication
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None
    
    authenticator, config = initialize_auth()
    
    if authenticator is None:
        return False, None, None, None
    
    # Check if already authenticated
    if st.session_state.get('authentication_status'):
        return True, st.session_state.get('username'), st.session_state.get('name'), authenticator
    
    # Display login page
    authentication_status, username, name = display_login_page()
    
    if authentication_status:
        st.session_state['authentication_status'] = True
        st.session_state['username'] = username
        st.session_state['name'] = name
        st.rerun()
        return True, username, name, authenticator
    
    return False, None, None, None

