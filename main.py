import os
from google import genai
from google.genai import types

# Initialize Gemini Client
API_KEY = os.environ.get('GEMINI_API_KEY', 'YOUR_API_KEY_HERE')
client = genai.Client(api_key=API_KEY)

def extract_action_items(raw_notes: str) -> str:
    """
    Parses unstructured meeting notes and extracts structured action items using Gemini API.
    """
    system_instruction = """
    You are an expert project management assistant.
    Your objective is to analyze unstructured meeting notes, emails, or chat logs 
    and extract a clean, actionable task plan.

    Required Output Format (Markdown):
    ## 🎯 Executive Summary
    (A brief 2-sentence summary of the main outcome)

    ## 📋 Action Items Matrix
    Create a Markdown table with the following columns:
    | Task | Assignee | Priority (High/Medium/Low) | Suggested Deadline |

    ## ⚠️ Identified Risks / Bottlenecks
    - List any risks, blockers, or critical dependencies mentioned.

    ## 💡 Immediate Next Steps
    - Urgent tasks to execute within the next 24-48 hours.
    """

    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=raw_notes,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
        ),
    )
    return response.text

if __name__ == "__main__":
    sample_meeting_notes = """
    Reunión de seguimiento del proyecto de migración - 07 Octubre.
    Estuvieron Juan, María y Carlos.
    Hablamos de que la base de datos sigue dando errores de latencia en hora pico.
    Carlos dice que puede revisar los índices del servidor pero necesita hasta el viernes porque está ocupado.
    María comentó que el cliente preguntó si la interfaz nueva estará lista la próxima semana.
    Juan no ha terminado los maquetados de Figma porque espera aprobación de presupuesto.
    Carlos necesita que Juan le envíe las credenciales de acceso al entorno de pruebas hoy mismo.
    Ojo: Si no se aprueba el presupuesto antes del jueves, todo el lanzamiento se retrasa 2 semanas.
    """

    print("Processing notes with Gemini API...\n")
    result = extract_action_items(sample_meeting_notes)
    print(result)
