#app/services/scorer_service.py
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate
from tenacity import retry, stop_after_attempt,wait_exponential
from app.config import setting

class ScoreResult(BaseModel):
    score:float
    reasoning:str
    correctness:float
    completeness:float
    clarity:float

PROMPT=ChatPromptTemplate(
    [SystemMessagePromptTemplate.from_template('You are an expert evaluator for AI-generated responses.'),
     HumanMessagePromptTemplate.from_template('''
                                                Given:
                                                - Question/Prompt: {prompt}
                                                - Model Response: {model_output}

                                                Evaluate the response on these criteria:
                                                - Correctness: Is the answer factually correct?
                                                - Completeness: Does it fully answer the question?
                                                - Clarity: Is it clear and well-expressed?

                                                Return a JSON with exactly these fields:
                                                {{
                                                    "score": <float between 0.0 and 1.0>,
                                                    "reasoning": "<brief explanation>",
                                                    "correctness": <float between 0.0 and 1.0>,
                                                    "completeness": <float between 0.0 and 1.0>,
                                                    "clarity": <float between 0.0 and 1.0>
                                                }}''')])
class ScoringError(Exception):
    pass

class ScorerService:
    def __init__(self):
        self.llm=ChatGoogleGenerativeAI(
            model='gemini-2.5-flash',   
            google_api_key=setting.google_api_key,
            request_timeout=10
        )

        self.structured_llm=self.llm.with_structured_output(ScoreResult)
        self.chain=PROMPT|self.structured_llm


    @retry(stop=stop_after_attempt(3),wait=wait_exponential(multiplier=1, min=2, max=10))
    def score(self,prompt:str,model_output:str)->ScoreResult:
        try:
            result=self.chain.invoke(
                {
                    'prompt':prompt,
                    'model_output':model_output
                }
            )
        except Exception as e:
            raise ScoringError(f"Error during scoring: {str(e)}") from e
        
        
        return result
    


