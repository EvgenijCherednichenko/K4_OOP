import os


class Settings:
    hh_vacancies_url = os.getenv("AUTH_URL", "https://api.hh.ru/vacancies")


settings = Settings()
