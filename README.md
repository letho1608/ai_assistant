# AI Assistant - Virtual Girlfriend

This project is an AI chatbot that plays the role of a virtual girlfriend, using the model from Ollama to interact in Vietnamese. The chatbot can answer questions about weather, news, open applications, and perform other tasks.

## System Requirements

- Python 3.x
- Ollama (Install the `Tuanpham/t-visstar-7b` model)
- Libraries: `speech_recognition`, `gTTS`, `requests`, `pygame`
You can change the model according to your language, machine configuration, and needs.
## Installation

1. **Install Python and required libraries**:

    ```bash
    pip install -r requirements.txt
    ```

2. **Install Ollama** and download the `Tuanpham/t-visstar-7b` model:

    ```bash
    ollama pull Tuanpham/t-visstar-7b
    ```

3. **Set up API Keys**:

    - Register at [OpenWeather](https://openweathermap.org/) and [NewsAPI](https://newsapi.org/), obtain API keys, and replace them in `main.py`.

4. **Change the city for weather**: Modify the `CITY` variable in `main.py` to specify the city for weather information.

    ```python
    CITY = ""  # Change this to your desired city
    ```

## Usage

1. **Run the application**:

    ```bash
    python main.py
    ```

2. **Voice commands**:
   - Ask about **weather**: "What is the weather today?"
   - Ask for **news**: "What's the latest news?"
   - **Open applications**: "Open Chrome", "Open Notepad"....
**And can ask or talk about different topics with her.**
**The chatbot will respond and perform actions using voice.**


