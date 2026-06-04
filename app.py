import streamlit as st
import os
import json
import random
import time
from datetime import datetime

# 모바일 화면 최적화 및 메타 설정 (v0.026 파이어베이스 전광판 동기화 에디션)
st.set_page_config(
    page_title="잇(it)시대를 즐기기",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------
# 🎨 글로벌 테마 CSS 최상단 격리
# -----------------------------------------------------------------
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ff9800, #f57c00);
        color: white; font-weight: bold; border-radius: 12px;
        padding: 16px; font-size: 18px; border: none;
        box-shadow: 0px 4px 10px rgba(245, 124, 0, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:active { transform: scale(0.98); }
    .status-box {
        background-color: #1e222b; padding: 22px; border-radius: 15px;
        border-left: 5px solid #ff9800; margin-bottom: 25px; line-height: 1.6;
    }
    .gm-box {
        background-color: #1a1c23; padding: 15px; border-radius: 12px;
        border: 2px dashed #00ffcc; color: #00ffcc; margin-bottom: 20px;
    }
    .stat-display { 
        background-color: #161b26; padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #233554; line-height: 1.8;
    }
    .cutscene-box {
        background-color: #2b1f1a; padding: 30px; border-radius: 15px;
        border: 2px solid #ffeb3b; text-align: center; margin-bottom: 25px;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 235, 59, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(255, 235, 59, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 235, 59, 0); }
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------
# 💾 서버 영구 저장 및 백엔드 로그 시스템
# -----------------------------------------------------------------
NOTICE_FILE = "gm_notice.txt"
MSG_FILE = "manager_messages.txt"
SAVE_FILE = "player_save.json"
LOG_FILE = "system_log.txt"

def get_rank_name(level):
    if level < 10: return "전산서기보 (9급) 시보 [초보자]"           # Rank 0
    elif level < 30: return "전산서기보 (9급) [전산실 막내]"         # Rank 1
    elif level < 50: return "전산서기 (8급) [행정망 해결사]"         # Rank 2
    elif level < 70: return "전산주사보 (7급) [과기 AI 주무관]"      # Rank 3
    elif level < 90: return "전산주사 (6급) [디지털보안팀장]"        # Rank 4
    elif level < 120: return "전산사무관 (5급) [SW정책과 차석]"      # Rank 5
    elif level < 150: return "전산서기관 (4급) [디지털정부기획과장]"   # Rank 6
    elif level < 180: return "전산부이사관 (3급) [디플정 본부장]"    # Rank 7
    elif level < 210: return "전산이사관 (2급) [국가정보자원관리원장]" # Rank 8
    elif level < 230: return "전산관리관 (1급) [국가 CTO]"           # Rank 9
    elif level < 250: return "디지털플랫폼정부위원회 위원장 (차관급)"  # Rank 10
    elif level < 270: return "과학기술정보통신부 장관 (장관급)"        # Rank 11
    elif level < 290: return "기획재정부 장관 겸 경제부총리"         # Rank 12
    elif level < 300: return "대한민국 국무총리 (행정부 2인자)"       # Rank 13
    else: return "대한민국 대통령 (👑 디지털 혁신 대통령)"           # Rank 14

def get_max_exp(level):
    if level >= 300: return 1
    return 100 + (level * 15)  

def append_log(event_type, details):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] [{event_type}] {details}\n")

def get_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return f.readlines()
    return ["아직 기록된 로그 데이터가 없습니다."]

def get_gm_notice():
    if os.path.exists(NOTICE_FILE):
        with open(NOTICE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return "현재 상시 사후지원 프로토콜이 가동 중입니다. 안전합니다."

def save_gm_notice(text):
    with open(NOTICE_FILE, "w", encoding="utf-8") as f:
        f.write(text)

def get_manager_messages():
    if os.path.exists(MSG_FILE):
        with open(MSG_FILE, "r", encoding="utf-8") as f:
            return f.readlines()
    return []

def append_manager_message(text):
    now = datetime.now().strftime("%H:%M:%S")
    with open(MSG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] 과장님: {text}\n")

def load_player_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "last_access" not in data: data["last_access"] = "기록 없음"
            if data.get("p_level", 1) > 300:
                data["p_level"] = 300
                data["guild_rank"] = get_rank_name(300)
                data["exp"] = get_max_exp(300)
            return data
    return {"exp": 0, "p_level": 1, "guild_rank": "전산서기보 (9급) 시보 [초보자]", "last_access": "기록 없음"}

def save_player_data(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 🚀 [추가 기능] Firebase 연동 X15 전광판 실시간 모니터링 컴포넌트
def render_gm_monitor():
    st.components.v1.html("""
    <div id="monitor-card" style="
        background-color: #1a1c23; border-radius: 12px; padding: 15px; 
        display: flex; align-items: center; justify-content: flex-start; gap: 20px;
        border: 1px solid #233554; border-left: 6px solid #00ffcc;
        color: white; font-family: 'Malgun Gothic', sans-serif;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3); margin-bottom: 5px;
    ">
        <div id="m-icon" style="font-size: 40px; min-width: 50px; text-align: center; text-shadow: 0 2px 5px rgba(0,0,0,0.5);">📡</div>
        <div style="display: flex; flex-direction: column; justify-content: center;">
            <span style="font-size: 13px; color: #aaa; font-weight: bold; margin-bottom: 5px; letter-spacing: -0.5px;">📡 GM강현 실시간 근무상황 (X15 전광판 동기화)</span>
            <span id="m-text" style="font-size: 22px; font-weight: 900; letter-spacing: -0.5px; color: #fff;">연결 중...</span>
        </div>
    </div>

    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-database.js"></script>
    <script>
        const firebaseConfig = {
            apiKey: "AIzaSyAP4Hcb0ORe-nWN1Rhg8F-DHZoAhJbRLcs",
            authDomain: "jyun-san-dh.firebaseapp.com",
            databaseURL: "https://jyun-san-dh-default-rtdb.firebaseio.com",
            projectId: "jyun-san-dh",
            storageBucket: "jyun-san-dh.firebasestorage.app",
            messagingSenderId: "683475811160",
            appId: "1:683475811160:web:ed9a340b98606fdef7032d"
        };
        if (!firebase.apps.length) {
            firebase.initializeApp(firebaseConfig);
        }
        const db = firebase.database();
        
        const stateMap = {
            "work_0": { text: "업무중", icon: "💻", color: "#1976d2" },
            "work_sweat": { text: "🔥땀내며 업무중", icon: "💦", color: "#d32f2f" },
            "work_1": { text: "전산 점검 중", icon: "🔧", color: "#f57c00" },
            "work_2": { text: "전산 장애 처리 중", icon: "🚨", color: "#d32f2f" },
            "work_3": { text: "출장", icon: "🚗", color: "#ffa000" },
            "work_4": { text: "전산 설치 중", icon: "🔌", color: "#f57c00" },
            "sec_1": { text: "보안점검 중", icon: "🛡️", color: "#d32f2f" },
            "call_1": { text: "착신", icon: "📞", color: "#0097a7" },
            "edu_1": { text: "전산 교육 중", icon: "📖", color: "#1976d2" },
            "away_1": { text: "외출", icon: "🚶", color: "#455a64" },
            "away_2": { text: "회의 중", icon: "🗣️", color: "#0097a7" },
            "away_3": { text: "잠깐 자리비움", icon: "☕", color: "#ffa000" },
            "night_1":{ text: "당직", icon: "🌙", color: "#303f9f" },
            "night_2":{ text: "당직 휴무", icon: "💤", color: "#455a64" },
            "lunch": { text: "점심 시간", icon: "🍱", color: "#1976d2" },
            "holiday":{ text: "오늘은 휴일입니다", icon: "🏡", color: "#455a64" },
            "blackout":{ text: "화면 보호 모드 (퇴근)", icon: "💤", color: "#222222" },
            "off_1": { text: "연가", icon: "🌴", color: "#455a64" },
            "off_2": { text: "병가", icon: "🏥", color: "#455a64" },
            "off_3": { text: "조퇴", icon: "🏃", color: "#455a64" }
        };

        db.ref('currentStatus').on('value', (snapshot) => {
            const val = snapshot.val();
            let id = "work_0";
            if (typeof val === 'string') id = val;
            else if (val && val.id) id = val.id;
            
            const state = stateMap[id] || { text: "상태 확인 중...", icon: "❓", color: "#455a64" };
            
            document.getElementById('m-icon').innerText = state.icon;
            document.getElementById('m-text').innerText = state.text;
            document.getElementById('monitor-card').style.borderLeftColor = state.color;
        });
    </script>
    """, height=110)

# -----------------------------------------------------------------
# 🛡️ 소스코드 크래킹 차단 방어막 (F12, 우클릭 제한)
# -----------------------------------------------------------------
st.components.v1.html("""
    <script>
    document.addEventListener('contextmenu', event => event.preventDefault());
    document.onkeydown = function(e) {
        if(e.keyCode == 123) { return false; }
        if(e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)) { return false; }
        if(e.ctrlKey && e.shiftKey && e.keyCode == 'C'.charCodeAt(0)) { return false; }
        if(e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)) { return false; }
    }
    </script>
""", height=0, width=0)

# -----------------------------------------------------------------
# 🔑 게이트웨이 인증 구조
# -----------------------------------------------------------------
if "user_role" not in st.session_state:
    st.session_state.user_role = None

if st.session_state.user_role is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("🔒 잇(it)시대를 즐기기")
    st.subheader("보안 시스템 검증 단계")
    st.write("지정된 자산 액세스 코드를 입력하여 시스템을 가동하세요.")

    user_password = st.text_input("액세스 코드 입력", type="password", placeholder="코드를 입력하세요")
    
    if st.button("인증 메커니즘 가동"):
        if user_password == "whrbehd": 
            st.session_state.user_role = "player"
            p_data = load_player_data()
            p_data["last_access"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_player_data(p_data)
            append_log("시스템 접속", "조규동 과장님이 대시보드에 진입하셨습니다.")
            st.rerun()
        elif user_password == "admin123":
            st.session_state.user_role = "admin"
            append_log("관리자 접속", "GM강현이 백엔드 제어 콘솔에 로그인했습니다.")
            st.rerun()
        else:
            st.error("❌ 접근 권한이 없습니다. 올바른 액세스 코드가 아닙니다.")

# -----------------------------------------------------------------
# 🕹️ [USER LAYER] 조규동 과장님 전용 런처 구역
# -----------------------------------------------------------------
elif st.session_state.user_role == "player":
    st.title("🎮 잇(it)시대를 즐기기")
    st.markdown("#### `VIP 전용 엔드게임 사후지원 플랫폼 v0.026`")
    st.write("---")

    current_notice = get_gm_notice()
    st.markdown(f"""
    <div class="gm-box">
        <span style='font-weight:bold;'>📡 GM강현의 실시간 지령:</span><br>
        <span style='font-size: 16px;'>" {current_notice} "</span>
    </div>
    """, unsafe_allow_html=True)

    # ⭐ X15 전광판 모니터 출력
    render_gm_monitor()

    player_data = load_player_data()
    
    st.markdown("### ⚡ 국가 디지털 혁신 능력 강화 훈련원")
    st.metric(label="현재 관직 스펙", value=f"Lv.{player_data['p_level']} {player_data['guild_rank']}")
    
    # 경험치 게이지 계산
    max_exp = get_max_exp(player_data['p_level'])
    current_exp = player_data['exp']
    if player_data['p_level'] >= 300:
        percent = 1.0
        exp_text = "MAX (대통령 도달)"
    else:
        percent = min(current_exp / max_exp, 1.0)
        exp_text = f"다음 레벨업까지: {current_exp} / {max_exp} ({(percent * 100):.1f}%)"
        
    st.progress(percent, text=exp_text)
    st.write("") 
    
    # ⭐ [컷신 모드] 직급 승진 시 버튼을 숨기고 강제 이펙트 뷰어 가동
    if st.session_state.get("is_job_advancing"):
        st.balloons()
        st.markdown(f"""
        <div class="cutscene-box">
            <h2>🎉 웅장한 빰빠레! 🎉</h2>
            <h4>과장님께서 <b>[{player_data['guild_rank']}]</b>(으)로 영전하셨습니다!</h4>
            <p style="color: #999;">⏳ 전직 이펙트 감상 중... (잠시 후 실무로 자동 복귀합니다)</p>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(3.0)
        st.session_state.is_job_advancing = False
        st.rerun()

    else:
        if st.session_state.get("level_up"):
            st.toast(f"✨ 폭풍 근무로 레벨 업 (Lv.{player_data['p_level']})!", icon="✨")
            st.session_state.level_up = False

        if st.button("💻 [폭풍 야근] 쉴 틈 없이 미친 듯이 실무 근무하기 💦"):
            if player_data['p_level'] >= 300:
                st.toast("👑 이미 국가 정점에 도달하여 더 이상 진급할 수 없습니다!")
            else:
                gain = random.randint(10, 25)
                player_data['exp'] += gain
                append_log("폭풍 근무", f"과장님이 폭풍 야근을 통해 경험치 {gain}을 획득했습니다.")
                
                if player_data['exp'] >= max_exp:
                    player_data['exp'] -= max_exp  
                    player_data['p_level'] += 1
                    new_rank = get_rank_name(player_data['p_level'])
                    
                    if new_rank != player_data['guild_rank']:
                        player_data['guild_rank'] = new_rank
                        st.session_state.is_job_advancing = True  
                        append_log("직급 승진", f"과장님이 Lv.{player_data['p_level']} [{player_data['guild_rank']}] 관직에 올랐습니다.")
                    else:
                        st.session_state.level_up = True
                
            save_player_data(player_data)
            st.rerun()

    st.write("---")

    with st.expander("🚀 메이플식 '디지털 혁신 대통령' 300레벨 전직 도감"):
        st.markdown("""
        **[0차] 공직 입문 튜토리얼 (Lv.1 ~ 9)**
        * **9급 전산서기보 시보:** 공무원의 첫걸음, 무자비한 수습기간을 버텨라!

        **[1차 전직] 실무 기술 전문가 과정 (Lv.10 ~ 89)**
        * **Lv.10~29 (9급 전산서기보):** 전산실 막내 / 국가 시스템 모니터링
        * **Lv.30~49 (8급 전산서기):** 행정망 유지보수 / 국가적 전산 장애 해결
        * **Lv.50~69 (7급 전산주사보):** 과기정통부 인공지능기반과 주무관
        * **Lv.70~89 (6급 전산주사):** 과기정통부 디지털보안팀장

        **[2차 전직] 디지털 정책 관리자 과정 (Lv.90 ~ 149)**
        * **Lv.90~119 (5급 전산사무관):** 소프트웨어정책과 차석 / 정책 기획
        * **Lv.120~149 (4급 전산서기관):** 디지털정부기획과장 / 'AI 행정망' 구축 주도

        **[3차 전직] 고위공무원단 및 국가 CTO (Lv.150 ~ 249)**
        * **Lv.150~179 (3급 전산부이사관):** 디플정 위원회 본부장
        * **Lv.180~209 (2급 전산이사관):** 국가정보자원관리원장 / 사이버 테러 방어
        * **Lv.210~249 (1급 전산관리관):** 과기정통부 정책실장 / 국가 CTO

        **[4차 전직] 국가 디지털 사령탑 (Lv.250 ~ 299)**
        * **Lv.250~269 (차관급):** 디지털플랫폼정부위원회 위원장
        * **Lv.270~289 (장관급):** 과학기술정보통신부 장관
        * **Lv.290~299 (부총리급):** 기획재정부 장관 겸 경제부총리

        **[최종 정점] 행정부 권력의 핵 (Lv.300 MAX)**
        * **Lv.300 대한민국 대통령:** 전산직 출신 최초의 국가원수
        """)

    st.write("---")

    st.markdown("### 🚨 실시간 핫라인 (GM 호출 창)")
    st.write("메시지를 남기거나, 공란으로 두고 버튼만 눌러도 전담 GM강현이 즉시 호출됩니다.")
    
    manager_text = st.text_input("전령 / 장애 신고 내용 입력:", placeholder="카톡 먹통, 알고리즘 이상 등 텍스트를 자유롭게 입력하세요.", key="m_text")
        
    if st.session_state.get("is_calling_gm"):
        st.snow()
        st.info("🚀 찌릿-! GM강현에게 전령이 빛의 속도로 날아가고 있습니다 🚀")
        time.sleep(2.5) 
        st.session_state.is_calling_gm = False
        st.rerun()
    else:
        if st.button("⚡ GM 호출하기"):
            if manager_text.strip():
                final_msg = f"[전송 메시지] {manager_text.strip()}"
            else:
                final_msg = f"[긴급 호출] 조규동 과장님이 즉시 호출을 요청하셨습니다."
                
            append_manager_message(final_msg)
            append_log("GM 호출", f"과장님이 GM을 호출했습니다: '{final_msg}'")
            st.session_state.is_calling_gm = True  
            st.rerun()

    st.write("---")

    st.markdown("""
    <div class="status-box">
        <h3 style='margin-top: 0;'>🏆 플레이어 고정 패시브 스펙</h3>
        <b>• 플레이어:</b> 조규동 과장님 <span style="color:#00ffcc;">(직업1 행정사무관 Level. MAX)</span><br><br>
        <b>• 영구 장착 타이틀:</b> <code style='color:#ff9800;'>신규 공무원의 등불</code>, <code style='color:#ff9800;'>인덕(人德) 만렙</code>, <code style='color:#ff9800;'>기다림의 미학 마스터</code><br><br>
        <b>• 상시 적용 버프:</b> GM강현의 평생 무상 전산 장애 사후지원 프로토콜
    </div>
    """, unsafe_allow_html=True)

    st.write("---")
    if st.button("🚪 시스템 안전 로그아웃"):
        append_log("세션 종료", "과장님이 메인 시스템에서 안전하게 로그아웃했습니다.")
        st.session_state.user_role = None
        st.rerun()

# -----------------------------------------------------------------
# 🛠️ [ADMIN LAYER] GM강현 전용 커스텀 제어실 구역
# -----------------------------------------------------------------
elif st.session_state.user_role == "admin":
    st.title("🛠️ GM강현 전용 제어 콘솔")
    st.markdown("#### `서버 백엔드 커널 및 라이브 모니터링 시스템`")
    st.write("---")

    # ⭐ X15 전광판 모니터 출력 (관리자 화면에서도 동기화)
    render_gm_monitor()

    player_data = load_player_data()
    
    st.markdown(f"""
    <div class='stat-display'>
        <h3 style='margin-top:0;'>📊 실시간 플레이어(과장님) 계정 매트릭스</h3>
        • <b>최근 대시보드 로그인 타임스탬프:</b> <code style='color:#00ffcc;'>{player_data['last_access']}</code><br><br>
        • <b>현재 원격 직급 상태:</b> {player_data['guild_rank']} (Lv.{player_data['p_level']})<br><br>
        • <b>현재 랭크 경험치 량:</b> {player_data['exp']} EXP
    </div>
    """, unsafe_allow_html=True)

    st.subheader("⚙️ 서버 레벨 및 스탯 강제 변조기")
    set_lv = st.number_input("대권 관직 강제 변조 (Lv.1 - Lv.300):", min_value=1, max_value=300, value=int(player_data['p_level']))
    set_exp = st.number_input("경험치(EXP) 강제 할당:", min_value=0, max_value=100000, value=int(player_data['exp']))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 입력한 밸런싱 값으로 서버 변조"):
            player_data['p_level'] = set_lv
            player_data['exp'] = set_exp
            player_data['guild_rank'] = get_rank_name(set_lv)
            save_player_data(player_data)
            append_log("스탯 변조", f"GM강현이 계정 데이터를 원격 변조했습니다. (Lv.{set_lv}, {set_exp} EXP)")
            st.success("데이터 강제 주입 성공!")
            st.rerun()
    with col2:
        if st.button("🚨 서버 세이브 데이터 공장 초기화"):
            init_data = {"exp": 0, "p_level": 1, "guild_rank": "전산서기보 (9급) 시보 [초보자]", "last_access": "데이터 리셋 완료"}
            save_player_data(init_data)
            append_log("데이터 초기화", "GM강현이 과장님의 세이브 파일을 초기화했습니다.")
            st.warning("서버의 모든 데이터가 초기화되어 9급 시보 막내 상태로 리셋되었습니다.")
            st.rerun()

    st.write("---")

    st.subheader("📡 서버 실시간 공지사항 원격 패치")
    new_notice = st.text_input("과장님 화면 상단 지령 전송 박스에 심어줄 메시지 입력:")
    if st.button("📡 전 서버 실시간 공지사항 배포 가동"):
        save_gm_notice(new_notice)
        append_log("공지 배포", f"GM공지가 실시간 업데이트되었습니다: '{new_notice}'")
        st.success("서버 동기화 가동! 과장님 화면에 실시간 브로드캐스팅 완료.")
        st.rerun()

    st.write("---")
    
    st.subheader("📜 시스템 실시간 블랙박스 작업 로그")
    logs = get_logs()
    log_text = "".join(logs[::-1])  
    st.text_area("Live Kernel Logs", value=log_text, height=180, disabled=True)

    st.write("---")
    
    st.subheader("📥 과장님이 실시간 발송한 전령 메시지 보관소")
    messages = get_manager_messages()
    if messages:
        for msg in messages[::-1]:  
            st.info(msg.strip())
    else:
        st.write("현재 서버 커널에 접수된 전령 데이터가 없습니다.")

    st.write("---")
    if st.button("🚪 GM 콘솔 세션 종료"):
        st.session_state.user_role = None
        st.rerun()
