import azure.functions as func
import logging
import os
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="cnt1/4180_001.pdf",
                               connection="pagesplitting9746_STORAGE") 
def blob_trigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    # Define the output folder
    output_folder = os.environ['AzureWebJobsScriptRoot']  # You can change this if needed

    # Split the PDF into single pages
    input_pdf_path = myblob.name
    input_stream = BytesIO(myblob.read())  # Create BytesIO object from bytes data
    input_pdf = PdfReader(input_stream)
    for page_num in range(len(input_pdf.pages)):
        output = PdfWriter()
        output.add_page(input_pdf.pages[page_num])
        
        # Define the "folder" based on the source PDF file
        folder_name = os.path.splitext(os.path.basename(input_pdf_path))[0]

        # Define the output PDF file path
        output_pdf_path = os.path.join(output_folder, folder_name, f"{os.path.basename(input_pdf_path)}_page_{page_num + 1}.pdf")

        # Ensure the "folder" structure exists in the output path
        os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

        # Write the PDF file to the output path
        with open(output_pdf_path, "wb") as output_stream:
            output.write(output_stream)
        logging.info(f"Page {page_num + 1} of {os.path.basename(input_pdf_path)} saved as {output_pdf_path}")

    # Log completion message
    logging.info(f"PDF {os.path.basename(input_pdf_path)} split into single pages")