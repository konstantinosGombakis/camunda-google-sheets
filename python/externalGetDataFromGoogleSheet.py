import logging
from concurrent.futures.thread import ThreadPoolExecutor

from camunda.external_task.external_task_worker import ExternalTaskWorker
from camunda.external_task.external_task import ExternalTask
from camunda.utils.log_utils import log_with_context

import gspread
import json

logger = logging.getLogger(__name__)

default_config = {
    "auth_basic": {"username": "demo", "password": "demo"},
    "maxTasks": 1,
    "lockDuration": 10000,
    "asyncResponseTimeout": 3000,
    "retries": 3,
    "retryTimeout": 5000,
    "sleepSeconds": 30,
    "isDebug": True,
    "httpTimeoutMillis": 3000,
}


with open('./cretential.json') as f:
    credentials = json.load(f)
 

gc = gspread.service_account_from_dict(credentials)

sh = gc.open_by_key("1jFHlcij79eiLlDhu2serhcn3ySSxmFrHb2bTYGpvHZg")


class TaskHandler:
    def __init__(self, sheet,cell):
        self.sheet = sheet
        self.cell = cell
        
    def set_cell(self,cell):
        self.cell = cell

    def handle_task(self, task: ExternalTask):
        # temperature = task.get_variable("temperature")
        worksheet = sh.sheet1
        # cell='B2'
        temperature=float(worksheet.acell(self.cell).value)
        temperature = temperature + 1
        print(f"Updated temperature: {temperature}")
        worksheet.update_acell(self.cell,temperature)
        return task.complete({"temperature": temperature})


def main():
    # configure_logging()
    handler = TaskHandler(sh, '')
    handler.set_cell('B2')
    topics = ["get_data_from_google_sheet"]
    executor = ThreadPoolExecutor(max_workers=len(topics))
    for index, topic in enumerate(topics):
        executor.submit(ExternalTaskWorker(worker_id=index, config=default_config).subscribe, topic, handler.handle_task)
    print("Finish Setting up")


def configure_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.StreamHandler()])


if __name__ == '__main__':
    main()
