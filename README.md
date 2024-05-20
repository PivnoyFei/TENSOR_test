<h1 align="center">TENSOR_test</h1>

### Стек:
![Python](https://img.shields.io/badge/Python-171515?style=flat-square&logo=Python)![3.12](https://img.shields.io/badge/3.12-blue?style=flat-square&logo=3.12)
![Pytest](https://img.shields.io/badge/Pytest-171515?style=flat-square&logo=Pytest)
![Selenium](https://img.shields.io/badge/Selenium-171515?style=flat-square&logo=Selenium)


### Запуск проекта
Клонируем репозиторий и переходим в него:
```bash
git clone https://github.com/PivnoyFei/TENSOR_test.git
cd TENSOR_test
```
Создаем виртуальное окружение:
```bash
python3 -m venv venv
```
Активируем виртуальное окружение:
```bash
source venv/bin/activate  # linux
```
```bash
source venv/Scripts/activate  # Windows
```
Ставим зависимости из requirements.txt:
```bash
pip install -r requirements.txt
```
Запускаем проект, откроет ссылку в браузере
```bash
pytest test.py
```