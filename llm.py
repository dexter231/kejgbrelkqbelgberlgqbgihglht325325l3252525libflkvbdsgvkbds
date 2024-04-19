import os
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API'))
# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

class gemini:
    def __init__(self,system_msg):
        self.history = []
        self.model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                generation_config=generation_config,
                                safety_settings=safety_settings,
                                system_instruction=system_msg)
        self.convo = self.model.start_chat()
    def reset(self):
        self.history=[]

    def get_response(self, input):
        self.convo.send_message(input)
        return self.convo.last.text


# llm = gemini("always reply in markdown")

# res=llm.get_response("hello")
# print(res)
