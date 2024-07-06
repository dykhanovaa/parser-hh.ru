import os
import time
import requests
import json
import webbrowser
from flask import Flask, render_template, url_for, request, redirect, session

app = Flask(__name__)
app.secret_key = os.urandom(24)  # секретный ключ для сессии

url = "https://api.hh.ru/vacancies"

# Функция main должна быть определена до использования в других частях кода
def main(vacancy_name, city, experience):
    experience_map = {
        'без опыта': 'noExperience',
        'от 1 года': 'between1And3',
        'от 3 лет': 'between3And6',
        'от 6 лет': 'moreThan6'
    }
    experience_param = experience_map.get(experience.lower(), 'noExperience')
    area_id = get_area_id(city)
    if not area_id:
        print(f"Город {city} не найден.")
        return []

    params = {
        'text': f'NAME:({vacancy_name})',
        'area': area_id,
        'experience': experience_param,
        'per_page': 100
    }

    data = get_vacancies(url, params)
    vacancies = parse_vacancies(data)
    print(f"Найдено {len(vacancies)} вакансий.")  # Добавить вывод для отладки
    return vacancies
    time.sleep(5)

def get_vacancies(url, params):
    all_vacancies = []
    page = 0
    while True:
        params['page'] = page
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if not data['items']:
                break
            all_vacancies.extend(data['items'])
            page += 1
        else:
            print(f"Ошибка: {response.status_code}")
            break
    return all_vacancies

def parse_vacancies(items):
    vacancies = []
    for item in items:
        salary = item.get('salary')
        vacancy = {
            'name': item.get('name'),
            'url': item.get('alternate_url'),
            'salary_from': salary.get('from') if salary else None,
            'salary_to': salary.get('to') if salary else None,
            'currency': salary.get('currency') if salary else None,
            'employer': item.get('employer', {}).get('name')
        }
        vacancies.append(vacancy)
    return vacancies

def get_area_id(city_name):
    areas_url = "https://api.hh.ru/areas"
    areas_response = requests.get(areas_url)
    if areas_response.status_code == 200:
        areas_data = areas_response.json()
        for country in areas_data:
            for area in country['areas']:
                if area['name'].lower() == city_name.lower():
                    return area['id']
                for sub_area in area['areas']:
                    if sub_area['name'].lower() == city_name.lower():
                        return sub_area['id']
    return None

@app.route('/vac')
def vacancies():
    vacancies = session.get('vacancies', [])
    print(f"Вакансии из сессии: {vacancies}")  # Добавить вывод для отладки
    return render_template('vacancies.html', vacancies=vacancies)

@app.route('/', methods=['GET', 'POST'])
def authorization():
    if request.method == 'POST':
        vacancy_name = request.form.get('vacancy_input')
        city = request.form.get('city_input')
        experience = request.form.get('exp_input')
        vacancies = main(vacancy_name, city, experience)
        session['vacancies'] = vacancies  # сохранить вакансии в сессии
        print(f"Сохранено в сессию: {vacancies}")  # Добавить вывод для отладки
        return redirect(url_for('vacancies'))

    return render_template('input.html')

def open_browser():
    webbrowser.open_new('http://127.0.0.1:8000/')

if __name__ == "__main__":
    open_browser()
    app.run(debug=True, port=8000)