from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.user import User
from app.repositories import run_repo
from app.schemas.run import RunCreate, RunUpdate
from app.utils.cache_utils import make_cache_key


class FakeRedis:
    def __init__(self):
        self.deleted = []

    def delete(self, key):
        self.deleted.append(key)


def make_session(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'runs.db'}"
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return TestingSessionLocal(), engine


def create_user(db, username):
    user = User(username=username, hashed_password="hashed")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_run_payload(prompt="Prompt", model_output="Output"):
    return RunCreate(
        experiment_id=1,
        prompt=prompt,
        model_output=model_output,
        model_name="gpt-test",
    )


def test_create_and_list_runs_are_scoped_to_user(tmp_path):
    db, engine = make_session(tmp_path)
    try:
        alice = create_user(db, "alice")
        bob = create_user(db, "bob")

        alice_run = run_repo.create_run(db, create_run_payload("A", "A out"), alice.id)
        bob_run = run_repo.create_run(db, create_run_payload("B", "B out"), bob.id)

        assert alice_run.user_id == alice.id
        assert bob_run.user_id == bob.id
        assert run_repo.get_runs(db, user_id=alice.id) == [alice_run]
        assert run_repo.get_runs(db, user_id=bob.id) == [bob_run]
    finally:
        db.close()
        engine.dispose()


def test_update_and_delete_require_matching_owner(tmp_path):
    db, engine = make_session(tmp_path)
    try:
        alice = create_user(db, "alice")
        bob = create_user(db, "bob")
        fake_redis = FakeRedis()
        run = run_repo.create_run(db, create_run_payload("Old prompt", "Old output"), alice.id)

        denied_update = run_repo.update_run(
            db,
            run.id,
            RunUpdate(prompt="Wrong owner"),
            fake_redis,
            user_id=bob.id,
        )
        assert denied_update is None

        updated = run_repo.update_run(
            db,
            run.id,
            RunUpdate(prompt="New prompt", status="completed"),
            fake_redis,
            user_id=alice.id,
        )
        assert updated.prompt == "New prompt"
        assert updated.status == "completed"
        assert fake_redis.deleted == [make_cache_key("Old prompt", "Old output")]

        assert run_repo.delete_run(db, run.id, user_id=bob.id) is False
        assert run_repo.get_run(db, run.id) is not None
        assert run_repo.delete_run(db, run.id, user_id=alice.id) is True
        assert run_repo.get_run(db, run.id) is None
    finally:
        db.close()
        engine.dispose()
