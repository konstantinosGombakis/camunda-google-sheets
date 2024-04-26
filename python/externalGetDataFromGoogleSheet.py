import logging
from concurrent.futures.thread import ThreadPoolExecutor

from camunda.external_task.external_task_worker import ExternalTaskWorker
from camunda.external_task.external_task import ExternalTask
from camunda.utils.log_utils import log_with_context

import uuid
from camunda.client.engine_client import EngineClient

import gspread
import json
import os

logger = logging.getLogger(__name__)

SERVER = os.getenv('MPMS_SERVER', 'localhost:8080')
print(f"Connecting to :{SERVER}")
USERNAME = os.getenv('MPMS_USERNAME', 'eurodyn')
PASSOWRD = os.getenv('MPMS_PASSOWRD', 'eurodyn')

default_config = {
    "auth_basic": {"username": USERNAME, "password": PASSOWRD},
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

business_key=uuid.uuid1()
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

    def resetGoogleSheetValues(self):
        worksheet = sh.sheet1
        worksheet.update_acell(self.cell,1)
        print(f"Setting value of cell {self.cell} to 1")
        print(f"See google sheet here: https://docs.google.com/spreadsheets/d/1jFHlcij79eiLlDhu2serhcn3ySSxmFrHb2bTYGpvHZg/edit?usp=sharing")

def start_proccess():
    client = EngineClient(engine_base_url='http://'+SERVER+'/engine-rest', config=default_config)
    resp_json = client.start_process(process_key="externalRaiseTemperature_google_sheet", business_key=str(business_key),variables={})
    process_instance=resp_json['id']
    print(f"See the running process: http://{SERVER}/camunda/app/cockpit/default/#/process-instance/{process_instance}")
    # print(resp_json)


def main():
    # configure_logging()
    handler = TaskHandler(sh, '')
    handler.set_cell('B2')
    handler.resetGoogleSheetValues()
    topics = ["get_data_from_google_sheet"]
    start_proccess()
    executor = ThreadPoolExecutor(max_workers=len(topics))
    for index, topic in enumerate(topics):
        executor.submit(ExternalTaskWorker(worker_id=index, base_url='http://'+SERVER+'/engine-rest', config=default_config).subscribe, topic, handler.handle_task)
    print("Finish Setting up...")


def configure_logging():
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.StreamHandler()])


if __name__ == '__main__':
    main()
