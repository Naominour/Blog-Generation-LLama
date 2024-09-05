# Generate Blogs with Streamlit and LLaMA 2
This project is a **Streamlit web application** that allows users to generate blogs on various topics using the **LLaMA 2 model**. Users can specify the number of words, the target audience, and the tone of the blog, making it a versatile tool for content creation.

### Sign up page:
<img src="images\img3.jpg" style="width:400px;border:solid 1px blue;">

### Blog generation page:
<img src="images\img1.jpg" style="width:400px;border:solid 1px blue;">


![LLaMA2](https://img.shields.io/badge/Skill-LLaMA2-yellow)
![LLM](https://img.shields.io/badge/Skill-LLM-blueviolet)
![Gen AI](https://img.shields.io/badge/Skill-Gen%20AI-orange)
![Conversational Bot](https://img.shields.io/badge/Skill-Conversational%20Bot-green)


## Features

- **Real-time Response:** The application interacts with the LLaMA 2 model to provide responses in real-time.
- **Tone Selection:** Choose from multiple tone options like Formal, Friendly, Casual, Professional, and more.
- **Customizable Blog Generation:** Generate blogs tailored to specific audiences such as Researchers, Data Scientists, and Common People.
- **Simple UI:** A user-friendly interface built with Streamlit, making it easy to generate content quickly.

## Installation
1. **Prerequisites**:
   - Python 3.8 or higher
   - LLama 2 Model

2. **Clone the Repository**:
```bash
git clone https://github.com/yourusername/generate-blogs.git
cd generate-blogs
```
3. **Set Up Virtual Environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
4. **Install Dependencies**:
```bash
pip install -r requirements.txt
```
5. **Download the LLaMA 2 model**:
   - Place the model downloaded file in the project directory.

6. **Running the Application**:
   - Run the Streamlit application using the following command:
```bash
streamlit run app.py
```

## Usage
- **Enter the blog topic:** Type in the topic you want to generate a blog about.
- **Specify the number of words:** Enter the desired word count for the blog.
- **Select the target audience:** Choose from Researchers, Data Scientists, or Common People.
- **Choose the tone:** Select the tone you want the blog to be written in, such as Formal, Friendly, Casual, etc.
- **Generate the blog:** Click on the "Generate" button to create the blog content.

## Customization
- **Background and Styling:** 
You can customize the background and styling of the application by modifying the CSS provided in the `st.markdown` section of the `app.py` file. The CSS is embedded directly into the Streamlit app to style elements like the background, buttons, and input fields.

- **Model Configuration:** 
You can tweak the model configuration (e.g., `max_new_tokens`, `temperature`) in the `getLLamaresponse` function to change how the LLaMA 2 model generates text. Adjusting these parameters can affect the creativity, coherence, and length of the generated content.
