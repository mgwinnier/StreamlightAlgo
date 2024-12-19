import os
import streamlit as st
from zipfile import ZipFile
from datetime import datetime
from main_script import run_scraping_tasks


def save_uploaded_file(uploaded_file, filename="data.txt"):
    """Save the uploaded file temporarily."""
    temp_path = os.path.join("./", filename)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_path


# Streamlit UI
st.title("NCAA Data Scraper and Processor")
st.subheader("Upload your `data.txt` file and select a date to run the scraper")

# File uploader
uploaded_file = st.file_uploader("Choose a `data.txt` file", type=["txt"])

# Date input
date_input = st.date_input("Select a date")

# Run button
if st.button("Run Scraper"):
    if uploaded_file and date_input:
        try:
            # Save the uploaded file temporarily
            temp_file_path = save_uploaded_file(uploaded_file)

            # Format the date
            formatted_date = date_input.strftime("%Y/%m/%d")

            # Run the main script
            st.write("Processing your request... This may take a few moments.")
            zip_file = run_scraping_tasks(formatted_date)

            # Serve the ZIP file for download
            if zip_file and os.path.exists(zip_file):
                with open(zip_file, "rb") as file:
                    st.download_button(
                        label="Download Results as ZIP",
                        data=file,
                        file_name=os.path.basename(zip_file),
                        mime="application/zip",
                    )
                st.success("Processing completed successfully!")
            else:
                st.error("Failed to generate the results ZIP file. Please try again.")

            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload a file and select a date.")
