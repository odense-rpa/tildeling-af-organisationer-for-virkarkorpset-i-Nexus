import asyncio
import logging
import sys
from datetime import datetime, timedelta

from automation_server_client import AutomationServer, Workqueue, WorkItemError, Credential, WorkItemStatus
from temponizer_client.manager import TemponizerClientManager
from proces.temponizer_service import TemponizerService
from proces.models import Vagt
from odk_tools.tracking import Tracker


temponizer: TemponizerClientManager
temponizer_service: TemponizerService




async def populate_queue(workqueue: Workqueue):
    logger = logging.getLogger(__name__)

    

    vagter = temponizer_service.hent_vagter()

    for vagt in vagter:
        if "education" in vagt:
            vikarinfo = temponizer_service.hent_vikar(vagt["workerId"])

        test = "test"





async def process_workqueue(workqueue: Workqueue):
    logger = logging.getLogger(__name__)

    logger.info("Hello from process workqueue!")

    for item in workqueue:
        with item:
            data = item.data  # Item data deserialized from json as dict
 
            try:
                # Process the item here
                pass
            except WorkItemError as e:
                # A WorkItemError represents a soft error that indicates the item should be passed to manual processing or a business logic fault
                logger.error(f"Error processing item: {data}. Error: {e}")
                item.fail(str(e))


if __name__ == "__main__":
    ats = AutomationServer.from_environment()
    workqueue = ats.workqueue()

    # Initialize external systems for automation here..

    tracking_credential = Credential.get_credential("Odense SQL Server")
    tracker = Tracker(
        username=tracking_credential.username, password=tracking_credential.password
    )

    temponizer_creds = Credential.get_credential("Temponizer - Roboa")
    temponizer = TemponizerClientManager(
        username=temponizer_creds.username,
        password=temponizer_creds.password,
        client_id=temponizer_creds.data["client-id"],
        client_secret=temponizer_creds.data["client-secret"],
        instance=temponizer_creds.data["instance"]
    )

    temponizer_service = TemponizerService(
        temponizer,
        tracker
    )

    # Queue management
    if "--queue" in sys.argv:
        workqueue.clear_workqueue(WorkItemStatus.NEW)
        asyncio.run(populate_queue(workqueue))
        exit(0)

    # Process workqueue
    asyncio.run(process_workqueue(workqueue))
