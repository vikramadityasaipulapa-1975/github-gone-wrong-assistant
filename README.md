GitHub Gone Wrong: AI Mentor Documentation

Overview
This application serves as an educational Socratic mentor for the "GitHub Gone Wrong: Rescue the Repository" hackathon event. Its primary objective is to help student participants troubleshoot and understand code concepts without handing out direct code solutions, bug fixes, or repository patches.

Core Guardrails Architecture
The app utilizes a dual-layer guardrail system to block direct code generation:
* System Instruction Level: Enforces a strict behavioral persona that instructs the model to act exclusively as an instructor, prohibiting code snippets, function fixes, or git diff solutions.
* Output Interception Layer (contains_forbidden_code): A programmatic Python validation filter that scans the model's raw response text for markdown code blocks (```) or git diff patterns (+ and - lines) and intercepts them before they reach the user interface.

Tech Stack
* Frontend/UI: Streamlit
* AI Model Engine: Google GenAI SDK (google-genai) utilizing gemini-3.6-flash

Local Installation & Setup Guide
1. Ensure Python 3.10 or higher is installed on your system.
2. Clone or download the repository containing assist-rails.py and requirements.txt.
3. Install the required dependencies via terminal:
   pip install -r requirements.txt
4. Set your Google Gemini API key as an environment variable:
   * Mac / Linux: export GEMINI_API_KEY="your_api_key_here"
   * Windows (Command Prompt): set GEMINI_API_KEY=your_api_key_here
5. Launch the local development server:
   streamlit run assist-rails.py

Cloud Deployment Instructions
* Platform: Streamlit Community Cloud (share.streamlit.io)
* Configuration: Link your GitHub repository, set the main entry point to assist-rails.py, and add your API key under the dashboard Secrets configuration as:
  GEMINI_API_KEY = "your_actual_api_key_here"