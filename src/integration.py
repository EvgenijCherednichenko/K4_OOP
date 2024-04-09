import abc
import requests
import typing as t
from .settings import settings


class VacancyParser(abc.ABC):
    """
    Abstract base class for vacancy parsers.
    """

    @abc.abstractmethod
    def get_vacancies(self):
        """
        Method to be implemented by subclasses to retrieve vacancies.

        Returns:
        List: A list of vacancies retrieved by the parser.
        """

        pass


class HHVacancyParser(VacancyParser):

    def __init__(self, headers: dict | None = None):
        self.headers = headers or {'User-Agent': 'HH-User-Agent'}

    def get_vacancies(self, keyword: str | None = None, page: int | None = None) -> dict:
        """
        Get vacancies from the API based on the keyword and page number.

        Args:
        - keyword (str | None): The keyword to search for in the vacancies. If None, all vacancies are returned.
        - page (int | None): The page number of the results to retrieve. If None, the first page is retrieved.

        Returns:
        - dict: The JSON response containing the vacancies from the API.
        """

        params = {"text": keyword, "page": page, "per_page": 100}
        response = requests.get(url=settings.hh_vacancies_url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()


class Vacancy:
    __slots__ = ('name', '_url', 'salary', 'description', 'requirements')

    def __init__(
            self, name: str, url: str | None = "",
            salary: dict | None = "",
            description: str | None = "", requirements: str | None = ""
    ):
        self.name = name
        self._url = url
        self.salary = salary
        self.description = description
        self.requirements = requirements

    @classmethod
    def json_to_object(cls, vacancies: dict) -> t.List["Vacancy"]:
        """
        Convert a dictionary of vacancies into a list of Vacancy objects.

        Args:
        - vacancies (dict): Dictionary containing vacancy information.

        Returns:
        - List["Vacancy"]: List of Vacancy objects created from the input dictionary.
        """

        return [
            Vacancy(
                vacancy.get("name"),
                url=vacancy.get("url"),
                salary=vacancy.get("salary"),
                description=vacancy.get("description"),
                requirements=vacancy.get("snippet").get("requirement")
            )
            for vacancy in vacancies.get("items")
        ]

    @staticmethod
    def is_filter_by_salary(
            salary_filter_value: int | None = None,
            vacancy_salary: dict | None = None
    ) -> bool:
        """
        Check if a salary filter value matches the vacancy's salary range.

        Args:
        - salary_filter_value (int | None): The salary filter value to compare against the vacancy's salary range.
        - vacancy_salary (dict | None): The dictionary containing the salary range of the vacancy.

        Returns:
        - bool: True if the vacancy's salary matches the filter value, False otherwise.
        """

        if not salary_filter_value:
            return True

        if vacancy_salary is None:
            return False
        source_salary, destination_salary = vacancy_salary.get("from"), vacancy_salary.get("to")

        if source_salary and not destination_salary:
            return salary_filter_value >= source_salary

        elif not source_salary and destination_salary:
            return salary_filter_value <= destination_salary

        elif source_salary and destination_salary:
            return source_salary <= salary_filter_value <= destination_salary

    @classmethod
    def filter_by_fields(cls, vacancies: t.List["Vacancy"], **kwargs):
        """
        Filter a list of vacancies based on provided criteria.

        Args:
        - vacancies (List["Vacancy"]): List of Vacancy objects to filter.
        - **kwargs: Keyword arguments for filtering criteria including name, url, salary, description, and requirements.

        Returns:
        - List["Vacancy"]: Filtered list of Vacancy objects based on the provided criteria.
        """

        name = kwargs.get("name", None)
        url = kwargs.get("url", None)
        salary = kwargs.get("salary")
        description = kwargs.get("description", None)
        requirements = kwargs.get("requirements", None)

        try:
            salary = int(salary) if salary else None
        except ValueError:
            salary = None

        filtered_vacancies = []
        for vacancy in vacancies:
            if (not name or vacancy.name == name) and \
                    (not url or vacancy._url == url) and \
                    cls.is_filter_by_salary(salary_filter_value=salary, vacancy_salary=vacancy.salary) and \
                    (not description or vacancy.description == description) and \
                    (not requirements or vacancy.requirements == requirements):
                filtered_vacancies.append(vacancy)

        return filtered_vacancies or vacancies

    @classmethod
    def serialized_vacancy(cls, vacancy: "Vacancy") -> dict:
        """
        Serialize a single Vacancy object into a dictionary.

        Args:
        - vacancy ("Vacancy"): The Vacancy object to be serialized.

        Returns:
        - dict: A dictionary representing the serialized vacancy with keys for name, url, salary, description, and requirements.
        """

        return {
            "name": vacancy.name,
            "url": vacancy._url,
            "salary": vacancy.salary,
            "description": vacancy.description,
            "requirements": vacancy.requirements
        }

    @classmethod
    def serialized_vacancies(cls, vacancies: t.List["Vacancy"]) -> t.List[dict]:
        """
        Serialize a list of vacancies into a list of dictionaries.

        Args:
        - vacancies (List["Vacancy"]): List of Vacancy objects to be serialized.

        Returns:
        - List[dict]: List of dictionaries representing the serialized vacancies.
        """

        return [cls.serialized_vacancy(vacancy) for vacancy in vacancies]

    def __gt__(self, other):

        """Метод сравнения вакансий между собой по зарплате и валидации данных по зарплате"""

        if self.salary is not None and other.salary is not None:
            if self.salary['to'] > other.salary['to']:
                return self
            else:
                return other
        return 'Зарплата не указана'

    def __lt__(self, other):

        """Метод сравнения вакансий между собой по зарплате и валидации данных по зарплате"""

        if self.salary is not None and other.salary is not None:
            if self.salary['to'] < other.salary['to']:
                return self
            else:
                return other
        return 'Зарплата не указана'
