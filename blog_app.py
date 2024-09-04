import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
import mysql.connector
from mysql.connector import Error

# Initialize Streamlit app
st.set_page_config(page_title="Blog Generation App", layout="centered")
st.title("AI Blog Generator")

# MySQL database connection function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Your MySQL host (use 'localhost' or an IP address)
            database='blog_db',  # Your database name
            user='root',  # Your MySQL username
            password='hessam'  # Your MySQL password
        )
        if connection.is_connected():
            st.success("Connected to MySQL database")
            return connection
    except Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None

# Initialize MySQL connection
connection = create_connection()

# Function to get response from LLama 2 model
def getLLamaresponse(input_text, no_words, blog_style, tone_style):
    llm = CTransformers(model='models/llama-2-7b-chat.ggmlv3.q8_0.bin', 
                        model_type='llama', 
                        config={'max_new_tokens': 256, 'temperature': 0.01})
    
    template = f"""
    Write a {tone_style} blog for {blog_style} job profile on the topic {input_text}
    within {no_words} words.
    """

    prompt = PromptTemplate(input_variables=["blog_style", "input_text", "no_words", "tone_style"],
                            template=template)

    response = llm.generate([prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words, tone_style=tone_style)])
    return response[0]

# User authentication state management
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

# Login function
def login(email, password):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    return user

# Sign Up form
def signup():
    st.subheader("Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, password))
        connection.commit()
        st.success("Sign Up successful! Please log in.")

# Login form
def login_form():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login(email, password)
        if user:
            st.session_state['user_id'] = user[0]
            st.success("Login successful!")
            st.experimental_rerun()  # Refresh the app
        else:
            st.error("Login failed. Please check your email and password.")

# Dashboard: Shows blogs for logged-in user
def dashboard():
    st.subheader("Your Blogs")
    user_id = st.session_state['user_id']
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM blogs WHERE user_id = %s", (user_id,))
    blogs = cursor.fetchall()

    for blog in blogs:
        st.write(f"### {blog[1]}")
        st.write(blog[2])

# Create Blog form
def create_blog():
    st.subheader("Create Blog")
    title = st.text_input("Blog Title")
    if st.button("Create Blog"):
        cursor = connection.cursor()
        cursor.execute("INSERT INTO blogs (user_id, title) VALUES (%s, %s)", 
                       (st.session_state['user_id'], title))
        connection.commit()
        st.success("Blog created!")
        st.experimental_rerun()

# AI Blog Generation form
def generate_blog():
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

# Main application logic
if st.session_state['user_id'] is None:
    st.write("Please log in or sign up.")
    login_form()
    if st.button("Go to Sign Up"):
        signup()
else:
    st.write(f"Welcome User {st.session_state['user_id']}")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({'user_id': None}))
    
    dashboard()
    create_blog()
    generate_blog()
