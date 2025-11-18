import google.generativeai as genai

genai.configure(api_key="AIzaSyBISBL4-8_hJZAsyJ_nO6B4CKDokXESIRQ")  # 👈 Replace this

model = genai.GenerativeModel("gemini-1.5-pro")

try:
    response = model.generate_content("Say hello from Gemini!")
    print(response.text)
except Exception as e:
    print("❌ Error:", e)
