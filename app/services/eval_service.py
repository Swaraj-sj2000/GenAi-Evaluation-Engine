#app/services/eval_service.py

from app.services.scorer_service  import ScorerService
from sqlalchemy.orm import Session
from app.models.run import Run
from app.utils.auth_utils import get_current_user
from app.schemas.run import RunResponse


class EvalService:
    def __init__(self):
        self.scorer=ScorerService()

    def evaluate(self,db:Session,run:Run)->Run:
        prompt=run.prompt
        model_output=run.model_output
        score_result=self.scorer.score(prompt,model_output)
        run.score=score_result.score
        run.status='completed'

        db.add(run)
        db.commit()
        db.refresh(run)
        return run
    
