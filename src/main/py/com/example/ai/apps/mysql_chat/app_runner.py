import os
import sys
from streamlit.web import cli as stcli
import uvicorn

def start_app():
    sys.argv = ["streamlit", "run", f"{os.environ['WORK_DIR']}/src/main/py/com/example/ai/apps/mysql_chat/app.py"]
    sys.exit(stcli.main())

def start_services():
    """Launched with `poetry run start`"""
    uvicorn.run("com.example.ai.apps.mysql_chat.main:app", host="0.0.0.0", port=8000, reload=True)