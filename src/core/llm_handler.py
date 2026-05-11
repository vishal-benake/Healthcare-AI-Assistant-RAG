from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.utils.prompts import SYSTEM_PROMPT
import json, re

class LLMHandler:
    def __init__(self):
        # Temperature 0 for strict JSON and medical accuracy
        self.llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

    def ask(self, context, question, memory=""):
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "CHAT HISTORY:\n{memory}\n\nCONTEXT:\n{context}\n\nQUESTION: {question}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"context": context, "question": question, "memory": memory})
        return self._parse_json(response.content)

    def _parse_json(self, text):
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            return json.loads(match.group(0)) if match else {"answer": text, "confidence": "low"}
        except:
            return {"answer": text, "confidence": "low", "sources": []}