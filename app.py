import app as st
import mysql.connector

from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from DBconnection import connection
from mysql.connector import Error

# Initialize Streamlit app
st.set_page_config(page_title="Blog Generation App", layout="centered")
st.title("AI Blog Generator")

# Function to get response from LLama 2 model
def getLLamaresponse(input_text, no_words, blog_style, tone_style):
    llm = CTransformers(model='/content/drive/MyDrive/Blog/models/llama-2-7b-chat.ggmlv3.q8_0.bin', 
                        model_type='llama', 
                        config={'max_new_tokens': 256, 'temperature': 0.01})
    
    template = f"""
    Write a {tone_style} blog for {blog_style} job profile on the topic {input_text}
    within {no_words} words.
    """

    prompt = PromptTemplate(input_variables=["blog_style", "input_text", "no_words", "tone_style"],
                            template=template)

    # Generate the response
    response = llm.generate([prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words, tone_style=tone_style)])
    
    # Extract the generated content from the response
    generated_text = response.generations[0][0].text
    return generated_text

# User authentication state management
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Manage form mode state (login, signup, dashboard)
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'  

# Login function
def login(email, password):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    return user

# Sign Up form
def signup():
    st.subheader("Sign Up")
    username = st.text_input("Username", key="signup_username")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, password))
        connection.commit()
        st.success("Sign Up successful! Please log in.")
        st.session_state['page'] = 'login'

# Login form
def login_form():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        user = login(email, password)
        if user:
            st.session_state['user_id'] = user[0]
            st.session_state['username'] = user[1]
            st.session_state['page'] = 'dashboard'
            st.success("Login successful!")
        else:
            st.error("Login failed. Please check your email and password.")

# Dashboard: Shows blog generation form and history in the sidebar
def dashboard():
    st.write(f"Welcome {st.session_state['username']}")

    # Blog generation form
    st.subheader("Generate AI Blog")
    input_text = st.text_input("Enter the topic of the blog")
    no_words = st.number_input("Number of words", min_value=50, max_value=500, value=150)
    blog_style = st.selectbox("Blog Style", ['Researchers', 'Data Scientist', 'Common People'])
    tone_style = st.selectbox("Tone Style", ['Formal', 'Friendly', 'Casual', 'Professional', 
                                             'Diplomatic', 'Confident', 'Engaging', 'Academic'])

    if st.button("Generate Blog"):
        generated_content = getLLamaresponse(input_text, no_words, blog_style, tone_style)
        st.subheader("Generated Blog")
        st.write(generated_content)

        # Save to database
        cursor = connection.cursor()
        cursor.execute("INSERT INTO blogs (user_id, title, content) VALUES (%s, %s, %s)", 
                       (st.session_state['user_id'], input_text, generated_content))
        connection.commit()
        st.success("Blog saved!")

    # Display blog history in the sidebar
    st.sidebar.subheader("Your Blog History")
    cursor = connection.cursor()
    cursor.execute("SELECT id, title FROM blogs WHERE user_id = %s", (st.session_state['user_id'],))
    blogs = cursor.fetchall()

    if blogs:
        for blog in blogs:
            if st.sidebar.button(blog[1]):
                show_blog(blog[0])
    else:
        st.sidebar.write("No blogs found.")

# Function to display a selected blog
def show_blog(blog_id):
    cursor = connection.cursor()
    cursor.execute("SELECT title, content FROM blogs WHERE id = %s", (blog_id,))
    blog = cursor.fetchone()
    st.subheader(blog[0])
    st.write(blog[1])

# Main application logic
if st.session_state['user_id'] is None:
    st.write("Please log in or sign up.")
    
    if st.session_state['page'] == 'login':
        login_form()
        if st.button("Go to Sign Up"):
            st.session_state['page'] = 'signup'
    elif st.session_state['page'] == 'signup':
        signup()
        if st.button("Go to Login"):
            st.session_state['page'] = 'login'
else:
    if st.session_state['page'] == 'dashboard':
        dashboard() 
        if st.sidebar.button("Logout"):
            st.session_state['user_id'] = None
            st.session_state['page'] = 'login'
