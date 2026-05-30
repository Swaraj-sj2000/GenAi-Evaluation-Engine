#app/services/eval_service.py


from app.services.scorer_service  import ScorerService
from sqlalchemy.orm import Session
from app.models.run import Run
from app.services.scorer_service import ScoreResult
from app.utils.cache_utils import make_cache_key

class EvalService:
    def __init__(self,scorer=None):
        self.scorer=scorer or ScorerService()

    
    def evaluate(self, db: Session, run: Run, redis_client ) -> Run:
        prompt=run.prompt
        model_output=run.model_output
        cache_key=make_cache_key(prompt,model_output)
        cached_score=redis_client.get(cache_key)
        if cached_score is not None:
            score_result = ScoreResult.model_validate_json(cached_score)
        
        else:
            score_result=self.scorer.score(prompt,model_output)
            redis_client.set(cache_key, score_result.model_dump_json(),ex=3600)

        run.score=score_result.score
        run.correctness=score_result.correctness
        run.completeness=score_result.completeness
        run.clarity=score_result.clarity
        run.status='completed'

        db.add(run)
        db.commit()
        db.refresh(run)
        return run
    
