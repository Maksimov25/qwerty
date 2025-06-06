# Система преобразования координат

Проект представляет собой веб-приложение для преобразования координат между различными системами (например, СК-42, ПЗ-90.11 и др.).

## 🚀 Развернутое приложение

Фронтенд (Streamlit):  
🔗 [https://qwerty-66k6r7kfrufbkhftz4j7hb.streamlit.app ](https://qwerty-66k6r7kfrufbkhftz4j7hb.streamlit.app )

Бэкенд (FastAPI):  
🔗 [https://qwerty-0ykp.onrender.com ](https://qwerty-0ykp.onrender.com )

---

## 📁 Структура проекта

## Структура проекта

```
.
├── backend/
│   └── main.py
├── frontend/
│   └── app.py
├── requirements.txt
└── README.md
```

## Возможности

- Загрузка Excel-файлов с координатными данными
- Преобразование координат с настраиваемыми параметрами
- Генерация отчетов в формате markdown
- Скачивание преобразованных данных и отчетов
- Современный веб-интерфейс на Streamlit
- REST API на FastAPI

## Инструкции по установке

### Локальная разработка

1. Клонируйте репозиторий:
```bash
git clone <url-репозитория>
cd coordinate-transformation-system
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Запустите бэкенд-сервер:
```bash
cd backend
uvicorn main:app --reload
```

4. Запустите фронтенд-приложение:
```bash
cd frontend
streamlit run app.py
```

### Развертывание

#### Бэкенд (Render.com)

1. Создайте новый Web Service на Render.com
2. Подключите ваш GitHub репозиторий
3. Установите следующие параметры:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Разверните сервис

#### Фронтенд (Streamlit Cloud)

1. Создайте аккаунт на Streamlit Cloud
2. Подключите ваш GitHub репозиторий
3. Установите следующие параметры:
   - Main file path: `frontend/app.py`
   - Python version: 3.9+
4. Обновите `BACKEND_URL` в `frontend/app.py`, указав URL вашего развернутого бэкенда
5. Разверните приложение

## Использование

1. Откройте Streamlit приложение в браузере
2. Загрузите Excel-файл с координатными данными (столбцы: x, y, z)
3. Настройте параметры преобразования
4. Нажмите "Преобразовать координаты"
5. Просмотрите и скачайте результаты
