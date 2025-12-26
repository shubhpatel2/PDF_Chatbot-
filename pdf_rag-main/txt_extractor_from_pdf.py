import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path, output_txt_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Extract text
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    
    # Save to a .txt file
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    
    print(f"✅ Text extracted and saved to: {output_txt_path}")

# Example usage
pdf_path = "Segment Anything.pdf"  # Make sure this file is in your working directory
output_txt_path = "output.txt"
extract_text_from_pdf(pdf_path, output_txt_path)
