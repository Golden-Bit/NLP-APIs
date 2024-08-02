import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path, text_format="text"):
    doc = fitz.open(pdf_path)  # Open the PDF file
    extracted_text = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text(text_format)
        extracted_text.append(text)

    #return "\n".join(extracted_text)
    return extracted_text

# Example usage
pdf_path = 'C:\\Users\\Golden Bit\\Downloads\\TKRPDTSgESr5GX18.pdf'
text_format = "dict"  # Extract text as dictionary, "text" for plain text, "html" for HTML, etc.

extracted_text = extract_text_from_pdf(pdf_path, text_format)

for dikt in extracted_text:
    blocks = dikt.get("blocks")#.keys())
    for block in blocks:
        print(block.keys())

