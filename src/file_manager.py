import abc
import csv
import json
import typing as t
from pathlib import Path


class BaseFileManager(abc.ABC):

    def __init__(self, output: str):
        """
        Initialize the class with the output file path.

        Args:
        - output: A string representing the path to the output CSV file.
        """
        self.output = Path(__file__).resolve().parent.parent / "data" / output

    @abc.abstractmethod
    def save(self, data):
        pass

    @abc.abstractmethod
    def add_object(self, data):
        pass

    @abc.abstractmethod
    def delete_object(self, data):
        pass


class JsonFileManager(BaseFileManager):

    def save(self, data: t.List[dict]):
        """
        Save a list of objects to a JSON file.

        Args:
        - data (List[dict]): List of dictionaries representing the objects to save.
        """
        with open(self.output, 'w', encoding='utf-8') as fp:
            json.dump(data, fp, ensure_ascii=False, indent=4)

    def add_object(self, data: dict) -> None:
        """
        Add a new object to the existing JSON file.

        Args:
        - data (dict): Dictionary representing the object to add.
        """
        with open(self.output, 'r', encoding='utf-8') as fp:
            file_data = json.load(fp)
        file_data.append(data)

        with open(self.output, 'w', encoding='utf-8') as fp:
            json.dump(file_data, fp, ensure_ascii=False, indent=4)

    def delete_object(self, data: dict) -> None:
        """
        Delete an object from the existing JSON file.

        Args:
        - data (dict): Dictionary representing the object to delete.
        """
        with open(self.output, 'r', encoding='utf-8') as fp:
            file_data = json.load(fp)
        file_data.remove(data)

        with open(self.output, 'w', encoding='utf-8') as fp:
            json.dump(file_data, fp, ensure_ascii=False, indent=4)


class CsvFileManager(BaseFileManager):

    def save(self, data: dict) -> None:
        """
        Saves the data to the CSV file.

        Args:
        - data: A list of dictionaries where each dictionary represents a row of data.

        Returns:
        - None
        """
        keys = data[0].keys()
        with open(self.output, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

    def add_object(self, data: dict) -> None:
        """
        Adds the specified object to the CSV file.

        Args:
        - data: A dictionary representing the object to be added to the CSV file.

        Returns:
        - None
        """
        with open(self.output, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)

        fieldnames = reader.fieldnames

        with open(self.output, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if csv_file.tell() == 0:
                writer.writeheader()

            rows.append(data)
            writer.writerows(rows)

    def delete_object(self, data: dict) -> None:
        """
        Deletes the specified object from the CSV file based on the data provided.

        Args:
        - data: A dictionary representing the object to be deleted from the CSV file.

        Returns:
        - None
        """
        with open(self.output, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [row for row in reader if row != data]

        with open(self.output, 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

