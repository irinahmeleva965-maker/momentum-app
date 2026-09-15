import streamlit as st
import time
import random

# Настройка страницы для мобильных
st.set_page_config(page_title="Сканер Моментума", page_icon="⚽", layout="centered")

# Функция для генерации звукового сигнала через браузер
def play_sound():
    sound_html = """
    <iframe src="https://mixkit.co" allow="autoplay" style="display:none"></iframe>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

st.title("⚽ Live Сканер Давления (Моментум)")
st.write("Приложение отслеживает давление в матчах онлайн и сигнализирует при опасности гола.")

# Имитация базы live-матчей
if 'matches' not in st.session_state:
    st.session_state.matches = [
        {"id": 1, "teams": "Реал Мадрид — Барселона", "score": "1:1", "minute": 72, "momentum": 45, "history": [10, 20, 30, 45]},
        {"id": 2, "teams": "Ливерпуль — Челси", "score": "0:0", "minute": 34, "momentum": 78, "history": [40, 55, 65, 78]},
        {"id": 3, "teams": "Бавария — Боруссия Д", "score": "2:0", "minute": 58, "momentum": -20, "history": [-10, -15, -18, -20]}
    ]

st.subheader("Текущие Live-Матчи")

# Логика обновления данных
for match in st.session_state.matches:
    # Немного меняем моментум для симуляции лайва
    change = random.randint(-15, 15)
    match["momentum"] = max(-100, min(100, match["momentum"] + change))
    if match["minute"] < 90:
        match["minute"] += 1
    match["history"].append(match["momentum"])
    if len(match["history"]) > 10:
        match["history"].pop(0)

    # Отрисовка матча
    st.markdown(f"**{match['teams']}** ({match['minute']}' мин) — Счет: `{match['score']}`")
    
    # Цвет в зависимости от моментума
    if abs(match["momentum"]) >= 70:
        st.error(f"💥 Критическое давление! Моментум: {match['momentum']}%")
    elif abs(match["momentum"]) >= 50:
        st.warning(f"⚠️ Растущее давление! Моментум: {match['momentum']}%")
    else:
        st.success(f" На равных. Моментум: {match['momentum']}%")

    # Прогресс-бар давления
    progress_val = int((match["momentum"] + 100) / 2)
    st.progress(progress_val)

    # ТРИГГЕР: Проверяем, близко ли гол (давление больше 70)
    if match["momentum"] >= 70:
        st.error(f"🚨 **ГОЛ НАЗРЕВАЕТ!** Первая команда зажала соперника!")
        play_sound()
    elif match["momentum"] <= -70:
        st.error(f"🚨 **ГОЛ НАЗРЕВАЕТ!** Вторая команда доминирует!")
        play_sound()
        
    st.divider()

# Автоперезагрузка страницы каждые 10 секунд
time.sleep(10)
st.rerun()
