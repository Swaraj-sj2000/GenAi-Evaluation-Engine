import os


os.environ["DATABASE_URL"] = "sqlite:////tmp/eval_engine_tests.db"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["DEBUG"] = "false"
os.environ["GOOGLE_API_KEY"] = "test-google-key"
os.environ["HUGGINGFACEHUB_API_KEY"] = "test-huggingface-key"
os.environ["LANGCHAIN_API_KEY"] = "test-langchain-key"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"
