# tests/test_langsmith.py

import os
from types import SimpleNamespace

from app.config import setting
import app.services.eval_service as eval_service_module
from app.services.eval_service import EvalService
from app.services.scorer_service import ScoreResult, ScorerService


class FakeDB:
    def __init__(self):
        self.added = []
        self.committed = False
        self.refreshed = []

    def add(self, item):
        self.added.append(item)

    def commit(self):
        self.committed = True

    def refresh(self, item):
        self.refreshed.append(item)


class FakeScorer:
    def score(self, prompt: str, model_output: str) -> ScoreResult:
        return ScoreResult(
            score=0.82,
            reasoning="The answer is mostly correct and clear.",
            correctness=0.9,
            completeness=0.75,
            clarity=0.8,
        )


class FakeRedis:
    def __init__(self):
        self.values = {}

    def get(self, key):
        return self.values.get(key)

    def set(self, key, value, ex=None):
        self.values[key] = value


def test_eval_service_updates_run_without_calling_llm(monkeypatch):
    monkeypatch.setattr(eval_service_module, "ScorerService", FakeScorer)
    fake_db = FakeDB()
    fake_run = SimpleNamespace(
        prompt="What is RAG?",
        model_output="RAG means retrieval augmented generation.",
        score=None,
        status="pending",
    )
    evaluator = EvalService()

    result = evaluator.evaluate(db=fake_db, run=fake_run, redis_client=FakeRedis())

    assert result is fake_run
    assert fake_run.score == 0.82
    assert fake_run.reasoning == "The answer is mostly correct and clear."
    assert fake_run.correctness == 0.9
    assert fake_run.completeness == 0.75
    assert fake_run.clarity == 0.8
    assert fake_run.status == "completed"
    assert fake_db.added == [fake_run]
    assert fake_db.committed is True
    assert fake_db.refreshed == [fake_run]


def run_manual_langsmith_trace():
    os.environ["LANGCHAIN_TRACING_V2"] = setting.langchain_tracing_v2
    os.environ["LANGCHAIN_API_KEY"] = setting.langchain_api_key
    os.environ["LANGCHAIN_PROJECT"] = setting.langchain_project

    scorer = ScorerService()
    result = scorer.score(
        prompt="What is the capital of France?",
        model_output="The capital of France is Paris.",
    )
    print(result)


if __name__ == "__main__":
    run_manual_langsmith_trace()
