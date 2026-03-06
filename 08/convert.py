import os
from pypdf import PdfReader
from gtts import gTTS

def extract_text_from_pdf(pdf_path: str):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"The file {pdf_path} is not found")
    
    reader = PdfReader(pdf_path)
    full_text=" "
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + " "
            
    clean_text = full_text.replace("/n", " ").replace("/r", "")
    return clean_text

def convert_text_to_audio(text: str, output_path: str, language:str = 'en'):
    if not text:
        raise ValueError("No text provided")
    
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(output_path)
    print(f"Audiobook successfully saved to {output_path}")
    
if __name__ == "__main__":
    # Test the script locally
    input_pdf = "Roadmap.pdf"   # Replace with a real PDF file path
    output_mp3 = "audiobook.mp3"

    try:
        print(f"Reading {input_pdf}...")
        extracted_text = extract_text_from_pdf(input_pdf)
        
        if extracted_text:
            convert_text_to_audio(extracted_text, output_mp3)
        else:
            print("No text could be extracted from the PDF.")
            
    except Exception as e:
        print(f"An error occurred: {e}")