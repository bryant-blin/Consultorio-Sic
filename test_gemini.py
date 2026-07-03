import google.generativeai as genai

# Configurar API Key
genai.configure(api_key="AQ.Ab8RN6L9E0IO0wuS3XupTXwj5-9KdgnNBjKU6-Or4PoZMUeYQQ")

print("=== 1. LISTANDO MODELOS DISPONIBLES EN TU CUENTA ===")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"❌ Error al listar modelos: {e}")

print("\n=== 2. PROBANDO CON 'gemini-1.5-flash' ===")
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Di: 'Prueba exitosa'")
    print(f"✅ Respuesta: {response.text.strip()}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n=== 3. PROBANDO CON 'gemini-1.5-flash-latest' ===")
try:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content("Di: 'Prueba exitosa'")
    print(f"✅ Respuesta: {response.text.strip()}")
except Exception as e:
    print(f"❌ Error: {e}")
