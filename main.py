from src.integration import HHVacancyParser, Vacancy
from src.file_manager import JsonFileManager

def get_vacancies():
    hh_api = HHVacancyParser()

    search_keyword = input("Введите поисковой запрос: ")
    hh_vacancies = hh_api.get_vacancies(keyword=search_keyword)

    vacancies_list = Vacancy.json_to_object(hh_vacancies)

    name_filter = input("Enter name to filter by (press Enter to skip): ")
    salary_filter = input("Enter salary to filter by (press Enter to skip): ")
    description_filter = input("Enter description to filter by (press Enter to skip): ")
    requirements_filter = input("Enter requirements to filter by (press Enter to skip): ")
    filters = {
        "name": name_filter, "salary": salary_filter,
        "description": description_filter, "requirements": requirements_filter
    }
    filtered_vacancies = Vacancy.filter_by_fields(vacancies_list, **filters)
    top_vacancies = int(input("Введите количество вакансий для вывода: "))

    top_filtered_vacancies = filtered_vacancies[:top_vacancies]
    serialized_vacancies = Vacancy.serialized_vacancies(top_filtered_vacancies)
    file_manager = JsonFileManager("vacancies.json")
    file_manager.save(serialized_vacancies)

    print(serialized_vacancies)


if __name__ == "__main__":
    get_vacancies()
