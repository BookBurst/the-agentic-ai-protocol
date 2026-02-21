import PyPDF2

def chew_pdf(file_path: str):
    # We open the binary PDF file.
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        full_text = ""
        # We iterate through every page to extract the raw text stream.
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
    return full_text

def semantic_split(document_text: str, max_length: int = 1000):
    # We split the raw text into natural paragraphs using double line breaks.
    # This keeps related ideas together in the same "mouthful."
    paragraphs = document_text.split("\n\n")
    memory_chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) < max_length:
            current_chunk += paragraph + "\n\n"
        else:
            memory_chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"
            
    if current_chunk:
        memory_chunks.append(current_chunk.strip())
    return memory_chunks

# EXECUTION PHASE
# 1. Extraction (Chewing)
raw_text = chew_pdf("company_handbook.pdf")
# 2. Slicing (Digestion)
final_chunks = semantic_split(raw_text)
