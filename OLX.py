import requests
from bs4 import BeautifulSoup

url = 'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/komplektuyuschie-i-aksesuary/q-%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BA%D0%B0%D1%80%D1%82%D1%8B-rtx/?currency=UAH&search%5Border%5D=filter_float_price:desc&search%5Bfilter_float_price:to%5D=5000'
page = 1  # начальная страница
file = open("output.txt", 'w')
seen_data = set()  # множество для хранения уникальных данных

while True:
    response = requests.get(url + f'&page={page}')

    if response.status_code == 200:
        # Создаем объект BeautifulSoup, указывая тип парсера
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим нужные элементы на странице
        elements = soup.find_all(class_='css-16v5mdi er34gjf0')
        elements_cel = soup.find_all(class_='css-10b0gli er34gjf0')

        # Проверяем, есть ли новые данные
        new_data = False
        for element, element_cel in zip(elements, elements_cel):
            data = element.text + '\n' + ' [ ' + element_cel.text + ' ] '

            if data not in seen_data:
                seen_data.add(data)
                print(element.text, element_cel.text)
                new_data = True
                file.write(data + '\n')

        # Если нет новых данных, значит достигнут конец списка страниц
        if not new_data:
            break
        page += 1  # переход на следующую страницу
    else:
        print('Ошибка при запросе к сайту')
        break