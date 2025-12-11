import re
from typing import List

from datetime import datetime, timedelta, timezone
import zoneinfo

from temponizer_client.manager import TemponizerClientManager
from temponizer_client.functionality.vagtplaner import PlanType
from odk_tools.tracking import Tracker

denmark_tz = zoneinfo.ZoneInfo("Europe/Copenhagen")

class TemponizerService:
    def __init__(
            self,
            temponizer: TemponizerClientManager,
            tracker: Tracker
            ):
        
        self.temponizer = temponizer
        self.tracker = tracker
    
    def hent_vagter(self) -> List[dict] :
        dagsdato = datetime.now()

        kommende_vagter = self.temponizer.vagtplaner.hent_vagtplan(dagsdato, dagsdato, PlanType.UPCOMING) or []
        
        igangværende_vagter = self.temponizer.vagtplaner.hent_vagtplan(dagsdato, dagsdato, plantype=PlanType.ONGOING) or []

        now = datetime.now(denmark_tz)
        today = now.date()
        
        # Combine both lists
        alle_vagter = kommende_vagter + igangværende_vagter
        
        # Filter for today's date, vikarkorpset, and within 2 hours
        relevante_vagter: List[dict] = []
        for vagt in alle_vagter:
            # Kontrol om det er vikarkorpset
            if not vagt["clientName"].lower().endswith("vikarkorpset"):
                continue
            
            # Kontrol af om vagten starter inden for de næste 2 timer
            # start_time = datetime.fromisoformat(vagt["startTime"]).astimezone(denmark_tz)
            # time_diff = start_time - now
            # if time_diff > timedelta(hours=2):
            #     continue
            
            relevante_vagter.append(vagt)
        
        return relevante_vagter
    
    def hent_vikar(self, vikarid: int) -> dict | None:

        vikar: dict | None = self.temponizer.medarbejder.hent_medarbejder(vikarid)

        return vikar
    