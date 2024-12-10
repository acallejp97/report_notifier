from retrievers.parking_retriever import ParkingRetriever
from retrievers.ester_retriever import EsterRetriever
from retrievers.abstract_retriever import AbstractRetriever
import os
import sys


def main():
    args = sys.argv
    service = get_service(args)
    service.process()


def get_service(args) -> AbstractRetriever:
    if args[1] == "parking":
        id_number = os.environ["ID_NUMBER"]
        has_changes = len(args) == 3 and args[2] == "has_changes"
        return ParkingRetriever(id_number=id_number, has_changes=has_changes)

    if args[1] == "ester":
        date = None if len(args) == 2 else args[2]
        return EsterRetriever(default_date=date)


if __name__ == "__main__":
    main()
