import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import base64
from io import BytesIO

BACKEND_URL = "http://localhost:8000"
API_URL = "http://localhost:8000"


st.set_page_config(page_title="Преобразование координат", layout="wide")
st.title("📍 Система преобразования координат")
st.markdown("Загрузите Excel-файл с координатами x, y, z для преобразования.")

# Получаем доступные системы
try:
    response = requests.get(f"{BACKEND_URL}/systems")
    if response.status_code == 200:
        systems = response.json().get("systems", [])
    else:
        st.error(f"Ошибка сервера: {response.status_code}")
        systems = ["СК-42", "ПЗ-90.11"]  # Значения по умолчанию
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
            data = {
                "sk1": initial_system,
                "sk2": target_system
                }
            response = requests.post(
            f"{BACKEND_URL}/transform",
            files=files,
            data=data
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    st.success("✅ Преобразование завершено!")
                    # Показываем результаты
                    excel_data = base64.b64decode(result["data"])
                    transformed_df = pd.read_excel(BytesIO(excel_data))
                    st.subheader("📊 Результаты преобразования")
                    st.dataframe(transformed_df)
                    
                    # Отчет
                    st.subheader("📄 Markdown отчет")
                    st.markdown(result["report"])
                    
                    # Кнопки скачивания
                    output_filename = f"transformed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                    st.download_button(
                        label="⬇️ Скачать результаты (Excel)",
                        data=excel_data,
                        file_name=output_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                    report_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                    st.download_button(
                        label="⬇️ Скачать отчет (Markdown)",
                        data=result["report"],
                        file_name=report_filename,
                        mime="text/markdown"
                    )
                else:
                    st.error(f"Ошибка: {result.get('message', 'Неизвестная ошибка')}")
            else:
                st.error(f"❌ Ошибка сервера: {response.text}")

    except Exception as e:
        st.error(f"❌ Ошибка: {str(e)}")