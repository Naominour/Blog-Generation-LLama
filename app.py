import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers

# Set the page configuration
st.set_page_config(page_title="Generate Blogs",
                   page_icon='🤖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

# Custom CSS for background color and font color
st.markdown("""
    <style>
    /* Change the entire body background */
    .main {
        background-color: #2E3C56;
        color: white;
    }
    /* Button styling */
    .stButton button {
        background-color: #E57A00;
        color: white;
    }
    /* Input and select boxes default styling */
    .stTextInput, .stSelectbox {
        background-color: white;
        color: black;
    }
    /* Change text color inside the input fields to black */
    .stTextInput > div > input, .stSelectbox > div > div > div {
        color: black !important;
        background-color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

## Function to get response from LLama 2 model
def getLLamaresponse(input_text,no_words,blog_style, tone_style):

    ### LLama2 model
    llm = CTransformers(model='/content/llama-2-7b-chat.ggmlv3.q8_0.bin', 
                        model_type='llama', 
                        config={'max_new_tokens':256, 'temperature':0.01})
    
    ## Prompt Template
    template = f"""
    Write a {tone_style} blog for {blog_style} job profile on the topic {input_text}
    within {no_words} words.
    """

    prompt = PromptTemplate(input_variables=["blog_style", "input_text", "no_words", "tone_style"],
                            template=template)

    ### Generate the response from the LLama 2 model
    response = llm.generate(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words, tone_style=tone_style))
    print(response)
    return response

st.header("Generate Blogs 🤖")

input_text = st.text_input("Enter the Blog Topic")

## Creating two more columns for additional 2 fields

col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words')
with col2:
    blog_style = st.selectbox('Writing the blog for',
                              ('Researchers', 'Data Scientist', 'Common People'), index=0)

# Adding a selectbox for tone style
tone_style = st.selectbox('Choose the tone of the blog',
                          ['👔 Formal', '🙂 Friendly', '😎 Casual', '💼 Professional', 
                           '🤝 Diplomatic', '💪 Confident', '👍 Engaging', '🎓 Academic'])

submit = st.button("Generate")

# Final response
if submit:
    st.write(getLLamaresponse(input_text, no_words, blog_style, tone_style))
