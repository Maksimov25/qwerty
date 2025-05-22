import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import base64
from io import BytesIO


BACKEND_URL = "http://localhost:8000"

st.title("📍 Система преобразования координат")
st.markdown("Загрузите Excel-файл с координатами x, y, z для преобразования.")

# Получаем доступные системы
try:
    response = requests.get(f"{BACKEND_URL}/systems")
    systems = response.json().get("systems", [])
except Exception as e:
    st.error(f"Не удалось загрузить системы: {e}")
    systems = ["СК-42", "ПЗ-90.11"]  # Значения по умолчанию

col1, col2 = st.columns(2)
with col1:
    initial_system = st.selectbox("Выберите начальную систему", systems)
with col2:
    target_system = st.selectbox("Выберите конечную систему", systems)

# Загрузка файла
uploaded_file = st.file_uploader("Выберите Excel-файл", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Предпросмотр данных
        df = pd.read_excel(uploaded_file)
        st.write("📥 Предпросмотр данных:")
        st.dataframe(df.head())

        # Отправка на бэкенд
        if st.button("🚀 Начать преобразование"):
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            }

            # Формируем URL с query-параметрами
            url = f"{BACKEND_URL}/transform?sk1={initial_system}&sk2={target_system}"
            response = requests.post(url, files=files)

            if response.status_code == 200 and response.json()["status"] == "success":
                result = response.json()
                # Показываем результаты
                st.success("✅ Преобразование завершено!")
                # Декодируем и читаем Excel-файл
                excel_data = base64.b64decode(result["data"])
                transformed_df = pd.read_excel(BytesIO(excel_data))
                st.subheader("📊 Результаты преобразования")
                st.dataframe(transformed_df)
                # Отчет
                st.subheader("📄 Markdown отчет")
                st.markdown(result["report"])
                # Кнопка скачивания
                transformed_df.to_excel("output.xlsx", index=False)
                with open("output.xlsx", "rb") as f:
                    st.download_button(
                        label="⬇️ Скачать результаты (Excel)",
                        data=f,
                        file_name=f"transformed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                with open("report.md", "w", encoding="utf-8") as f:
                    f.write(result["report"])
                with open("report.md", "rb") as f:
                    st.download_button(
                        label="⬇️ Скачать отчет (Markdown)",
                        data=f,
                        file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
            else:
                st.error(f"❌ Ошибка сервера: {response.text}")
    except Exception as e:
        st.error(f"❌ Ошибка: {str(e)}")