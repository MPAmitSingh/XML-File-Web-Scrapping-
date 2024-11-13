# import library
import streamlit as st # for web design
import xml.etree.ElementTree as ET # used for parsing, creating, and modifying XML data.
import re # regular expression
from bs4 import BeautifulSoup #library is primarily used for parsing and extracting information from HTML and XML documents.
from io import BytesIO # for download the file

# Titel for the app
st.title("XML Text Extractor")
# description
st.write("This app processes XML text and converts it into clean, readable text, removing unnecessary tags and formatting for easier use and analysis. Simply input your XML data, and the app will extract the content in a streamlined format")

# Input field for XML content

# File uploader to select XML file
uploaded_file = st.file_uploader("Choose an XML file", type=["xml"])

if uploaded_file is not None:
    if st.button("Convert"):
        try:
           
            # Parse XML from the uploaded file
            tree = ET.parse(uploaded_file)
            root = tree.getroot()
            # Convert XML root element to a string for processing
            root_str = ET.tostring(root, encoding='utf8').decode('utf8')
            
            # Define text cleaning functions
            def strip_html(text):
                soup = BeautifulSoup(text, "html.parser")
                return soup.get_text()

            def remove_between_square_brackets(text):
                return re.sub(r'\[[^]]*\]', '', text)

            def denoise_text(text):
                text = strip_html(text)
                text = remove_between_square_brackets(text)
                text = re.sub('  ', '', text)
                return text

            # Cleaned output
            sample = denoise_text(root_str)
            st.write("Text Cleaned Sucessfully.")
            st.success(sample)
            
            # conver the clean text to wownloadable format
            download_data=BytesIO(sample.encode())
            
            # creat a down load button to donwload it text file
            st.download_button(
                label="Download Cleaned Text",
                data=download_data,
                file_name="Clean_text.txt",
                mime="text/plain"
                )
            st.write("Thanks for using This...")
        except ET.ParseError:
            st.error("Invalid XML format. Please check your input.")
            