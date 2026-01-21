from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st 
import google.generativeai as genai
from agents.pdf2text import text_extractor
from agents.word2text import doc_text_extract
from agents.image2text import extract_text_image

# lets configure genai model
gemini_key = os.getenv('GOOGLE_API_KEY1')
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite',
                              generation_config={'temperature':0.9}) 

# lets create the sidebar

st.sidebar.title(':red[UPLOAD YOUR NOTES:]')
st.sidebar.subheader(':blue[Only upload Images, PDFs and DOCX]')
user_file = st.sidebar.file_uploader('Upload Here:', type=['pdf','docx','jpeg','jpg','jfif'])

if user_file:
    st.sidebar.success('File Uploaded Successfully')
    if user_file.type == 'application/pdf':
        user_text = doc_text_extract(user_file)
    elif user_file.type in ['image/jpeg','image/png','image/jpg','image/jfif']:
        user_text = extract_text_image(user_file)
    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text = text_extractor(user_file)

# Lets create main page
st.title(':orange[MoM Generator:] :blue[AI Assisted Minutes of Meeting Generator]')
st.subheader(':green[This application creates generalised minutes of the meeting]')
st.write('''
         Follow these steps:
         1. Upload the notes in PDF, DOCX, or Image Format in the sidebar.
         2. Click "Generate" to generate the MoM.
         ''')

if st.button('Generate'):
    with st.spinner('Please wait...'):
        prompt = f'''
        <Role> You are an expert in writing and formatting minutes of meeting
        <Goal> Create minutes of meeting from the notes that user has provided.
        
        <Context> The user has provided some rough notes as text. Here are the notes: {user_text}
        
        <Format> The output must follow the below format
        * Title: assume title of the meeting.
        * Agenda: assume agenda of the meeting.
        * Attendees: Name of the attendees (If name of the attendees is not there, keep it NA)
        * Date and Place: date and the place of the meeting (If not provided, keep it Online)
        * Body: the body should follow the below sequence of points
            * Mention Key points discussed.
            * Highlight any decision that has been taken.
            * Mention Actionable items.
            * Mention any deadline (if discussed).
            * Mention Next meeting date (if discussed)
            * Add a 2-3 line of summary.
            
        <Instructions>
        * Use bullet points and highlight the important keywords by making them bold wherever possible.
        * Generate the output in docx format
        '''
        
        response = model.generate_content(prompt)
        st.write(response.text)
        
    if st.download_button(label = 'DOWNLOAD',
                          data = response.text,
                          file_name='mom_generated.text',
                          mime = 'text/plain'):
        st.success('Your file is downloaded')