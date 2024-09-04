from flask import Flask, request, render_template, redirect, url_for, session, flash
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = ''

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
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print("Error connecting to MySQL database", e)
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

@app.route('/')
def home():
    return redirect(url_for('login'))

# Sign Up Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, password))
        connection.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

# Sign In Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash("Login failed. Please check your email and password.")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM blogs WHERE user_id = %s", (user_id,))
    blogs = cursor.fetchall()

    return render_template('dashboard.html', blogs=blogs)

@app.route('/create_blog', methods=['GET', 'POST'])
def create_blog():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        user_id = session['user_id']

        cursor = connection.cursor()
        cursor.execute("INSERT INTO blogs (user_id, title) VALUES (%s, %s)", 
                       (user_id, title))
        connection.commit()
        return redirect(url_for('dashboard'))
    
    return render_template('create_blog.html')

# Route for AI Blog Generation
@app.route('/generate_blog', methods=['GET', 'POST'])
def generate_blog():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        input_text = request.form['input_text']
        no_words = request.form['no_words']
        blog_style = request.form['blog_style']
        tone_style = request.form['tone_style']

        # Generate content using Llama 2
        generated_content = getLLamaresponse(input_text, no_words, blog_style, tone_style)
        
        # Save generated blog to the database
        user_id = session['user_id']
        cursor = connection.cursor()
        cursor.execute("INSERT INTO blogs (user_id, title, content) VALUES (%s, %s, %s)", 
                       (user_id, input_text, generated_content))
        connection.commit()

        return redirect(url_for('dashboard'))
    
    blog_styles = ['Researchers', 'Data Scientist', 'Common People']
    tone_styles = ['Formal', 'Friendly', 'Casual', 'Professional', 
                   'Diplomatic', 'Confident', 'Engaging', 'Academic']

    return render_template('generate_blog.html', blog_styles=blog_styles, tone_styles=tone_styles)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
