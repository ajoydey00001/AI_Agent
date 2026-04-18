
import os
from dotenv import load_dotenv
import yaml
try:
    from pyprojroot import here
except Exception:
    # Minimal fallback for `here()` when pyprojroot isn't installed.
    # Assumes repository layout where this file is located at <repo>/src/utils/...
    from pathlib import Path

    def here(p=""):
        root = Path(__file__).resolve().parents[2]
        return root / p if p else root
import shutil
# AzureOpenAI and AzureChatOpenAI have moved between packages across
# langchain versions. Import defensively so this module can be imported
# even if those providers aren't installed in the environment.
try:
    from openai import AzureOpenAI
except Exception:
    AzureOpenAI = None

try:
    # Newer langchain versions may provide the class under langchain.chat_models
    from langchain.chat_models import AzureChatOpenAI
except Exception:
    try:
        # Some installs use the separate langchain_openai package
        from langchain_openai import AzureChatOpenAI
    except Exception:
        AzureChatOpenAI = None

try:
    import chromadb
except Exception:
    chromadb = None

print("Environment variables are loaded:", load_dotenv())


class LoadConfig:
    def __init__(self) -> None:
        with open(here("configs/app_config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        self.load_directories(app_config=app_config)
        self.load_llm_configs(app_config=app_config)
        # self.load_openai_models()
        self.load_chroma_client()
        self.load_rag_config(app_config=app_config)

        # Un comment the code below if you want to clean up the upload csv SQL DB on every fresh run of the chatbot. (if it exists)
        # self.remove_directory(self.uploaded_files_sqldb_directory)

    def load_directories(self, app_config):
        self.stored_csv_xlsx_directory = here(
            app_config["directories"]["stored_csv_xlsx_directory"])
        self.sqldb_directory = str(here(
            app_config["directories"]["sqldb_directory"]))
        self.uploaded_files_sqldb_directory = str(here(
            app_config["directories"]["uploaded_files_sqldb_directory"]))
        self.stored_csv_xlsx_sqldb_directory = str(here(
            app_config["directories"]["stored_csv_xlsx_sqldb_directory"]))
        self.persist_directory = app_config["directories"]["persist_directory"]

    def load_llm_configs(self, app_config):
        self.model_name = os.getenv("gpt_deployment_name")
        self.agent_llm_system_role = app_config["llm_config"]["agent_llm_system_role"]
        self.rag_llm_system_role = app_config["llm_config"]["rag_llm_system_role"]
        self.temperature = app_config["llm_config"]["temperature"]
        self.embedding_model_name = os.getenv("embed_deployment_name")

    # def load_openai_models(self):
    #     azure_openai_api_key = os.environ["OPENAI_API_KEY"]
    #     azure_openai_endpoint = os.environ["OPENAI_API_BASE"]
    #     # This will be used for the GPT and embedding models
    #     self.azure_openai_client = AzureOpenAI(
    #         api_key=azure_openai_api_key,
    #         api_version=os.getenv("OPENAI_API_VERSION"),
    #         azure_endpoint=azure_openai_endpoint
    #     )
    #     self.langchain_llm = AzureChatOpenAI(
    #         openai_api_version=os.getenv("OPENAI_API_VERSION"),
    #         azure_deployment=self.model_name,
    #         model_name=self.model_name,
    #         temperature=self.temperature)

    def load_chroma_client(self):
        if chromadb is None:
            # chromadb isn't installed in this environment; make this optional so
            # scripts that don't require the vector DB can still run.
            print("chromadb not available: skipping Chroma client initialization.")
            self.chroma_client = None
            return

        self.chroma_client = chromadb.PersistentClient(
            path=str(here(self.persist_directory)))

    def load_rag_config(self, app_config):
        self.collection_name = app_config["rag_config"]["collection_name"]
        self.top_k = app_config["rag_config"]["top_k"]

    def remove_directory(self, directory_path: str):
        """
        Removes the specified directory.

        Parameters:
            directory_path (str): The path of the directory to be removed.

        Raises:
            OSError: If an error occurs during the directory removal process.

        Returns:
            None
        """
        if os.path.exists(directory_path):
            try:
                shutil.rmtree(directory_path)
                print(
                    f"The directory '{directory_path}' has been successfully removed.")
            except OSError as e:
                print(f"Error: {e}")
        else:
            print(f"The directory '{directory_path}' does not exist.")
