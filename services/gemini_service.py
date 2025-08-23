from google.generativeai import configure, GenerativeModel
from config.gemini_config import get_gemini_config
from prompts.system_instruction_gemini import build_system_instruction


class GeminiService:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._initialize(cls._instance)
        return cls._instance

    @staticmethod
    def _initialize(instance):
        config = get_gemini_config()
        configure(api_key=config["api_key"])

        system_instruction = build_system_instruction()
        instance._model = GenerativeModel(
            model_name=config["model_name"],
            system_instruction=system_instruction
        )

    def get_response(self, prompt: str) -> str:
        try:
            response = self._model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error al generar respuesta: {str(e)}"

    @classmethod
    def reset_instance(cls):
        cls._instance = None
