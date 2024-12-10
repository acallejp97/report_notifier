from notification_service import NotificationService
from retrievers.abstract_retriever import AbstractRetriever
import requests
from bs4 import BeautifulSoup
from constants import BILBAO_PARKING_URL
from save_file_service import SaveService


class ParkingRetriever(AbstractRetriever):
    def __init__(self, id_number: str, has_changes: bool = False):
        self.has_changes = has_changes
        self.id_number = id_number
        self.save_service = SaveService("parking_position.txt")

    def process(self):
        user_list = self.get_parking_list()
        position = self.filter_list(user_list)
        self.save_service.save([position])
        if not self.has_changes or self.save_service.read() != position:
            self.create_response(position)

    def filter_list(self, user_list):
        for element in user_list:
            if element["ID_NUMBER"] == self.get_hidden_id():
                return element["position"]

    def get_hidden_id(self):
        hidden_id = f"****{self.id_number[-5:]}"
        return hidden_id[:-1] + "*"

    def create_response(self, value):
        NotificationService().send_message("Lista Parking Rekalde", f"Estás el numero {value} en la lista")

    @staticmethod
    def get_parking_list():
        r = requests.get(BILBAO_PARKING_URL)
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table")
        parking_list = []
        if table:
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                cols = [ele.text.strip() for ele in cols]
                if len(cols) != 0:
                    formatted_row = {
                        "position": cols[0],
                        "ID_NUMBER": cols[2],
                    }
                    parking_list.append(formatted_row)
        return parking_list
