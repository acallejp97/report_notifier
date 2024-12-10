import requests
from datetime import date
from retrievers.abstract_retriever import AbstractRetriever
from notification_service import NotificationService
from constants import ESTER_URL


class EsterRetriever(AbstractRetriever):
    def __init__(self, default_date: str) -> None:
        self.date = self.yesterday(default_date)

    def process(self):
        value = self.get_ester_value()
        self.create_response(value)

    def get_ester_value(self):
        response = requests.get(ESTER_URL).json()
        clean_json = self.clear_json(response)
        for response in clean_json:
            if response["PERIOD"].split("T")[0] == self.date:
                return response

    def create_response(self, value: dict):
        NotificationService().send_message(
            "Indice €STER",
            f"El valor del €STER para el dia {self.original_date(self.date)} es {value['OBS']}. En comparación con el dia anterior ha tenido una tendencia {value['TREND_INDICATOR']}",
        )

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
    def yesterday(selected_date: str):
        today = date.today() if selected_date is None else date.fromisoformat(selected_date)
        yesterday = today.replace(day=today.day - 1)
        return yesterday.strftime("%Y-%m-%d")

    @staticmethod
    def original_date(date_string: str):
        date_object = date.fromisoformat(date_string)
        day_plus_one = date_object.replace(day=date_object.day + 1)
        return day_plus_one.strftime("%Y-%m-%d")
