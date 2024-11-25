"""
This Python program is designed to automate the extraction and analysis of feedback from `.pdf` files stored in a specified folder. 
It scans the folder for `.pdf` files, extracts the text content from each document, and analyzes the feedback to identify potential issues or areas for improvement. 
Using regular expressions, the program detects keywords related to bugs, performance issues, inaccuracies, and positive feedback, generating specific action recommendations. 
After analyzing all the feedback, the program compiles the results into a new `.pdf` document, summarizing the updates and suggested actions for each feedback source.

The primary goal of this program is to streamline the process of reviewing and addressing feedback for a system, such as a custom GPT model or similar AI application. 
It eliminates the need for manual review by automating the extraction of key insights from large numbers of feedback documents. 
This can significantly improve efficiency, especially when managing a large volume of user feedback. 
The outputted `.pdf` provides a clear, structured report that highlights the feedback and suggests concrete next steps for developers or system administrators, facilitating prompt action on identified issues and ensuring that valuable positive feedback is recognized and utilized for further enhancements.
"""

import os
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import re

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
    return text

# Function to analyze the feedback and suggest actions
def analyze_feedback(feedback_text):
    recommendations = []
    
    if re.search(r"(bug|error|issue)", feedback_text, re.I):
        recommendations.append("Investigate the reported bug or error.")
    
    if re.search(r"(slow|delay)", feedback_text, re.I):
        recommendations.append("Consider optimizing response time or processing power.")
    
    if re.search(r"(inaccurate|wrong|incorrect)", feedback_text, re.I):
        recommendations.append("Refine the model's prompt engineering and training data.")
    
    if re.search(r"(good|excellent|amazing)", feedback_text, re.I):
        recommendations.append("Great feedback! Consider further enhancing these features.")

    if not recommendations:
        recommendations.append("No immediate actions required. Continue monitoring feedback.")
    
    return recommendations

# Function to generate a PDF with the analysis updates
def generate_pdf(updates, output_pdf_path):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter

    # Start writing content on the PDF
    c.setFont("Helvetica", 10)
    y_position = height - 40  # Start at the top of the page

    # Add Title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, y_position, "Feedback Analysis Updates")
    y_position -= 20

    # Add each update recommendation to the PDF
    c.setFont("Helvetica", 10)
    for update in updates:
        if y_position < 40:  # Check if there's space for more content, otherwise create a new page
            c.showPage()
            c.setFont("Helvetica", 10)
            y_position = height - 40
        c.drawString(30, y_position, update)
        y_position -= 15
    
    # Save the PDF file
    c.save()

# Main function to process all PDFs in the folder and generate an update PDF
def main(input_folder, output_pdf_path):
    updates = []
    
    # Loop through all the files in the folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            print(f"Processing PDF: {filename}")

            # Extract text from the PDF
            feedback_text = extract_text_from_pdf(pdf_path)
            print(f"Feedback Text: {feedback_text[:200]}...")  # Preview the first 200 characters of the text
            
            # Analyze the feedback
            recommendations = analyze_feedback(feedback_text)
            
            # Add the recommendations to the updates list
            updates.append(f"Feedback from {filename}:")
            for recommendation in recommendations:
                updates.append(f"  - {recommendation}")
            updates.append("")  # Add a blank line after each set of recommendations
    
    # Generate the output PDF with the updates
    generate_pdf(updates, output_pdf_path)
    print(f"Output PDF generated: {output_pdf_path}")

# Run the script
input_folder = "path_to_your_folder_containing_pdfs"
output_pdf_path = "feedback_updates.pdf"
main(input_folder, output_pdf_path)
