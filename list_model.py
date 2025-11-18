import google.generativeai as genai

genai.configure(api_key="AIzaSyBISBL4-8_hJZAsyJ_nO6B4CKDokXESIRQ")  # replace with your real key

for m in genai.list_models():
    print(m.name)
