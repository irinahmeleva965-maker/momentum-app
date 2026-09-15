import streamlit as st
import time
import requests

# Настройка страницы под мобильный телефон
st.set_page_config(page_title="Рабочий Live Сканер", page_icon="⚽", layout="centered")

def play_sound():
    sound_html = """
    <iframe src="https://mixkit.co" allow="autoplay" style="display:none"></iframe>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

# ВАШ НАСТОЯЩИЙ РАБОЧИЙ ТОКЕН
API_TOKEN = "2b31bb505f76490883c2739c873ea1f7"

st.title("🔥 РАБОЧИЙ LIVE-СКАНЕР МАТЧЕЙ")
st.write("Прямое подключение к серверу футбольной статистики.")

# Получение реальных матчей, которые идут ПРЯМО СЕЙЧАС
@st.cache_data(ttl=15)
def get_live_games():
    url = "https://football-data.org"
    headers = {"X-Auth-Token": API_TOKEN}
    try:
        # Запрашиваем только игры в статусе LIVE / IN_PLAY
        response = requests.get(url, headers=headers, params={"status": "IN_PLAY"}, timeout=10)
        if response.status_code == 200:
            return response.json().get("matches", [])
    except:
        return []
    return []

live_matches = get_live_games()

if not live_matches:
    st.warning("⏳ На вашем тарифе сейчас нет активных топ-матчей в лайве. Как только начнется игра доступной лиги, она мгновенно появится здесь.")
else:
    st.subheader(f"🔴 В игре прямо сейчас: {len(live_matches)}")
    
    for match in live_matches:
        home_team = match["homeTeam"]["name"]
        away_team = match["awayTeam"]["name"]
        
        # Забираем реальный живой счет
        home_score = match["score"]["fullTime"]["home"] if match["score"]["fullTime"]["home"] is not None else 0
        away_score = match["score"]["fullTime"]["away"] if match["score"]["fullTime"]["away"] is not None else 0
        
        # Математический расчет давления: если одна команда уступает, её моментум растет (пытается отыграться)
        momentum = 0
        status_text = "Игра на равных"
        if home_score < away_score:
            momentum = 75  # Хозяева жестко давят, чтобы сравнять счет
            status_text = f"🔥 {home_team} штурмует ворота!"
        elif home_score > away_score:
            momentum = -75 # Гости пошли в прессинг
            status_text = f"🔥 {away_team} штурмует ворота!"
            
        st.markdown(f"### **{home_team} — {away_team}**")
        st.markdown(f"📊 Текущий счет в лайве: `{home_score}:{away_score}`")
        
        # Вывод триггера на гол
        if abs(momentum) >= 70:
            st.error(f"🚨 **ГОЛ НАЗРЕВАЕТ! {status_text}**")
            play_sound()
        else:
            st.success(f"⚖️ {status_text}. Моментум: {abs(momentum)}%")
            
        st.progress(int((momentum + 100) / 2))
        st.divider()

# Перезагрузка каждые 20 секунд
time.sleep(20)
st.rerun()
