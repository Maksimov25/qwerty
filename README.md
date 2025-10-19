# Система преобразования координат

Проект представляет собой веб-приложение для преобразования координат между различными системами (например, СК-42, ПЗ-90.11 и др.).

## Развернутое приложение

Фронтенд (Streamlit):  
🔗 [https://qwerty-66k6r7kfrufbkhftz4j7hb.streamlit.app ](https://qwerty-66k6r7kfrufbkhftz4j7hb.streamlit.app )

Бэкенд (FastAPI):  
🔗 [https://qwerty-0ykp.onrender.com ](https://qwerty-0ykp.onrender.com )

---

## Структура проекта

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



### Локальная разработка

git clone <url-репозитория>
cd coordinate-transformation-system

python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
pip install -r requirements.txt

cd backend
uvicorn main:app --reload

cd frontend
streamlit run app.py
```

### Развертывание

#### Бэкенд (Render.com)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
Разверните сервис

#### Фронтенд (Streamlit Cloud)

   - Main file path: `frontend/app.py`
   - Python version: 3.9+
Обновите `BACKEND_URL` 
Разверните приложение
