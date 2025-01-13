from datetime import date
from datetime import datetime

import requests
from constants import ESTER_URL
from retrievers.abstract_retriever import AbstractRetriever


class EsterRetriever(AbstractRetriever):
    def __init__(self, default_date: str) -> None:
        super().__init__()
        self.date = self.yesterdays_value(default_date)

    def process(self):
        value, found = self.get_ester_value()
        self.create_response([value, found])

    def get_ester_value(self):
        response = requests.get(ESTER_URL).json()
        clean_json = self.clear_json(response)
        for response in clean_json:
            if response["PERIOD"].split("T")[0] == self.date:
                return [response, True]
        return [response, False]

    def create_response(self, value):
        value, found = value
        if not found:
            message = f"El ultimo valor del €STER registrado es {value['OBS']} para el dia {value['PERIOD']}. Su tendencia para dicho dia era {value['TREND_INDICATOR']}"
        else:
            message = f"El valor del €STER para el dia {self.original_date(self.date)} es {value['OBS']}. En comparación con el dia anterior ha tenido una tendencia {value['TREND_INDICATOR']}."
            if datetime.now().hour < 4:
                message = (
                    message
                    + "\nEl valor del €STER se actualiza diariamente a las 4:00 AM. Se ha tomado el valor del dia anterior."
                )
        self.notification_service.send_message("Indice €STER", message)

    @staticmethod
    def clear_json(json: list):
        past_value = 0
        for registry in json:
            if registry["OBS"] is None:
                registry["OBS"] = past_value
                registry["OBS_VALUE_ENTITY"] = past_value
                registry["TREND_INDICATOR"] = "equal"
            past_value = registry["OBS"]
        json.reverse()
        return json

    @staticmethod
    def yesterdays_value(selected_date: str):
        today = date.today() if selected_date is None else date.fromisoformat(selected_date)
        remove_day = 1 if datetime.now().hour > 4 else 2
        yesterdays_value = today.replace(day=today.day - remove_day)
        return yesterdays_value.strftime("%Y-%m-%d")

    @staticmethod
    def original_date(date_string: str):
        date_object = date.fromisoformat(date_string)
        add_day = 1 if datetime.now().hour > 4 else 2
        day_plus_one = date_object.replace(day=date_object.day + add_day)
        return day_plus_one.strftime("%Y-%m-%d")
