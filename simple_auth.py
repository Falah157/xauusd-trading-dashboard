"""
Simple Authentication Module
============================
A simplified authentication system without external dependencies
to avoid widget key conflicts.
"""

import streamlit as st
import hashlib
import json
import os


def hash_password(password):
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    """Load users from a simple JSON file."""
    users_file = "users.json"
    if os.path.exists(users_file):
        try:
            with open(users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    else:
        # Create default demo user
        default_users = {
            "demo": {
                "password": hash_password("demo123"),
                "name": "Demo User",
                "email": "demo@goldtrading.com"
            }
        }
        save_users(default_users)
        return default_users


def save_users(users):
    """Save users to JSON file."""
    with open("users.json", "w") as f:
        json.dump(users, f)


def authenticate_user(username, password):
    """Authenticate user credentials."""
    users = load_users()
    if username in users:
        hashed_password = hash_password(password)
        if users[username]["password"] == hashed_password:
            return True, users[username]
    return False, None


def display_login_page():
    """Display login page with custom styling."""
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
    
    # Login form
    with st.form("login_form_simple"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Login", use_container_width=True)
        
        if submitted:
            if username and password:
                success, user_info = authenticate_user(username, password)
                if success:
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.session_state['name'] = user_info['name']
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please enter both username and password")
    
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
        signup_form_simple()


def signup_form_simple():
    """Display signup form for new users."""
    st.subheader("Register New User")
    
    with st.form("signup_form_simple"):
        new_username = st.text_input("Username", key="signup_username")
        new_name = st.text_input("Full Name", key="signup_name")
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
        
        submitted = st.form_submit_button("Create Account")
        
        if submitted:
            # Validation
            if not all([new_username, new_name, new_email, new_password, confirm_password]):
                st.error("All fields are required!")
                return
            
            if new_password != confirm_password:
                st.error("Passwords do not match!")
                return
            
            users = load_users()
            if new_username in users:
                st.error("Username already exists!")
                return
            
            # Add new user
            users[new_username] = {
                "password": hash_password(new_password),
                "name": new_name,
                "email": new_email
            }
            
            save_users(users)
            st.success("Account created successfully! Please login with your credentials.")


def display_logout_button():
    """Display logout button in sidebar."""
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
            <p style="color: white; margin: 5px 0 0 0; font-size: 18px; font-weight: bold;">{st.session_state.get('name', 'User')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            # Clear session state
            for key in list(st.session_state.keys()):
                if key in ['authenticated', 'username', 'name']:
                    del st.session_state[key]
            st.rerun()


def check_authentication():
    """Check if user is authenticated."""
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if st.session_state['authenticated']:
        return True, st.session_state.get('username'), st.session_state.get('name')
    else:
        display_login_page()
        return False, None, None
