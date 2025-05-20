import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import base64
from io import BytesIO

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Преобразование координат", layout="wide")
st.title("📍 Система преобразования координат")
st.markdown("Загрузите Excel-файл с координатами x, y, z для преобразования.")

# Получаем доступные системы
try:
    response = requests.get(f"{BACKEND_URL}/systems")
    systems = response.json().get("systems", [])
except Exception as e:
    st.warning(f"Не удалось загрузить системы (используются тестовые): {e}")
    systems = ["СК-42", "ПЗ-90.11"]

col1, col2 = st.columns(2)
with col1:
    initial_system = st.selectbox("Выберите начальную систему", systems)
with col2:
    target_system = st.selectbox("Выберите конечную систему", systems)

uploaded_file = st.file_uploader("Выберите Excel-файл", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.write("📥 Предпросмотр данных:")
        st.dataframe(df.head())

        if st.button("🚀 Начать преобразование"):
            with st.spinner('Идет преобразование координат...'):
                response = requests.post(
                    f"{BACKEND_URL}/transform",
                    params={"sk1": initial_system, "sk2": target_system},
                    files={"file": (uploaded_file.name, uploaded_file.getvalue())}
                )

            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    st.success("✅ Преобразование завершено!")

                    # Обработка результатов
                    excel_data = base64.b64decode(result["data"])
                    transformed_df = pd.read_excel(BytesIO(excel_data))

                    st.subheader("📊 Результаты преобразования")
                    st.dataframe(transformed_df)

                    st.subheader("📄 Отчет")
                    st.markdown(result["report"])

                    # Кнопки скачивания
                    st.download_button(
                        label="⬇️ Скачать результаты (Excel)",
                        data=excel_data,
                        file_name=f"transformed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                    st.download_button(
                        label="⬇️ Скачать отчет (Markdown)",
                        data=result["report"],
                        file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                else:
                    st.error(f"Ошибка преобразования: {result.get('message')}")
            else:
                st.error(f"Ошибка сервера: {response.text}")
    except Exception as e:
        st.error(f"❌ Ошибка: {str(e)}")