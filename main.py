# main.py
import streamlit as st
import re
from scrapping import (
    scrapping_the_website,
    remove_dom_content,
    unwanted_content,
    split_dom_content
)
from ollama_parse import parsing_with_ollama

# Step 1: Enhance URL validation function
def is_valid_url(url):
    pattern = re.compile(r'^(https?://)?([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,6})([/a-zA-Z0-9#?&=-]*)?$')
    return re.match(pattern, url) is not None

# Step 2: Create the UI with enhancements
st.title("Wrapo - Web Scraping and Parsing Tool")

# Initialize session state with an empty string if not already present
if 'url' not in st.session_state:
    st.session_state.url = ''
if 'dom_content' not in st.session_state:
    st.session_state.dom_content = None

# Sidebar for URL input and additional settings
with st.sidebar:
    url = st.text_input("Enter URL", value=st.session_state.url)
    if not is_valid_url(url) and url:
        st.warning("Please enter a valid URL.")
    st.session_state.url = url

    # Option to select parsing method
    parse_method = st.selectbox("Choose Parsing Method", ["Ollama", "Custom Extractor", "Basic Extractor"])

# Step 3: Add scraping and parsing functionality
if st.button("Scrape Website"):
    if url:
        with st.spinner('Scraping the website...'):
            dom_content = scrapping_the_website(url)  # Get raw DOM content
            body_content = remove_dom_content(dom_content)  # Clean body content
            cleaned_content = unwanted_content(body_content)  # Remove unwanted content

            st.session_state.dom_content = cleaned_content  # Store cleaned content in session state
            st.success("Website scraped successfully!")

        # Display the DOM content with a collapsible section
        with st.expander("View Scraped DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)

# Step 4: Add functionality to parse and display results
if "dom_content" in st.session_state:
    parse_description = st.text_area("What do you want to parse?", height=100)

    # Progress bar while parsing
    if parse_description and st.button("Parse"):
        with st.spinner('Parsing the content...'):
            dom_chunks = split_dom_content(st.session_state.dom_content)  # Split content for parsing
            if parse_method == "Ollama":
                result = parsing_with_ollama(dom_chunks, parse_description)
            elif parse_method == "Custom Extractor":
                result = "Custom parsing result (to be implemented)"
            else:
                result = "Basic extraction (to be implemented)"
            st.write(result)

# Step 5: Add additional features
if st.button("Download Cleaned Content"):
    if st.session_state.dom_content:
        st.download_button(
            label="Download Cleaned Content",
            data=st.session_state.dom_content,
            file_name="cleaned_content.txt",
            mime="text/plain"
        )

# Search functionality
search_term = st.text_input("Search in DOM Content")
if search_term and st.session_state.dom_content:
    search_results = [line for line in st.session_state.dom_content.split("\n") if search_term.lower() in line.lower()]
    if search_results:
        st.write("Search Results:")
        st.write("\n".join(search_results))
    else:
        st.write("No results found.")

# Step 6: Feedback form to collect user input
with st.expander("Provide Feedback"):
    feedback = st.text_area("Share your feedback about the app:")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")

# Step 7: Summary or sentiment analysis (Optional for future implementation)
# Implement a feature to summarize or analyze sentiment of the content
if st.button("Summarize Content"):
    if st.session_state.dom_content:
        summary = "Summary of content (to be implemented)"
        st.write(summary)
