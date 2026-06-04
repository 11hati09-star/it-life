import streamlit as st
import os
import json
from datetime import datetime

# 모바일 화면 최적화 설정
st.set_page_config(
    page_title="잇(IT) 시대를 즐기기",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------
# 💾 서버 영구 저장 파일 시스템 (DB 대용 JSON & TXT)
# -----------------------------------------------------------------
NOTICE_FILE = "gm_notice.txt"
MSG_FILE = "manager_messages.txt"
SAVE_FILE = "player_save.json"

# 1. GM -> 과장님 지령
def get_gm_notice():
    if os.path.exists(NOTICE_FILE):
        with open(NOTICE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return "현재 상시 사후지원 프로토콜이 가동 중입니다. 안전합니다."

def save_gm_notice(text):
    with open(NOTICE_FILE, "w", encoding="utf-8") as f:
        f.write(text)

# 2. 과장님 -> GM 전령
def get_manager_messages():
    if os.path.exists(MSG_FILE):
        with open(MSG_FILE, "r", encoding="utf-8") as f:
            return f.readlines()
    return []

def append_manager_message(text):
    now = datetime.now().strftime("%H:%M:%S")
    with open(MSG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] 과장님: {text}\n")

# 3. ⭐ 플레이어 세이브 데이터 영구 로드/저장 함수
def load_player_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # 세이브 파일이 없을 때의 초기값 (레벨 1)
    return {"exp": 0, "p_level": 1, "guild_rank": "동해 오피스 소속"}

def save_player_data(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# -----------------------------------------------------------------
# 🛡️ 프론트엔드 방어막 (우클릭 및 소스코드 차단)
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
# 🔑 VIP 인증 시스템 (비밀번호: qkrdudcjf)
# -----------------------------------------------------------------
if "password_correct" not in st.session_state:
    st.session_state.password_correct = False

def check_password():
    if st.session_state.password_correct:
        return True

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("🔒 잇(IT) 시대를 즐기기")
    st.subheader("VIP 전용 인증 시스템")
    user_password = st.text_input("액세스 코드 입력", type="password", placeholder="비밀번호를 입력하세요")
    
    if st.button("인증 메커니즘 가동"):
        if user_password == "qkrdudcjf": 
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("❌ 접근 권한이 없습니다. 지정된 VIP가 아닙니다.")
    return False

# -----------------------------------------------------------------
# 메인 어플리케이션 구역
# -----------------------------------------------------------------
if check_password():

    # MMORPG 테마 스타일 시트
    st.markdown("""
        <style>
        .main { background-color: #0e1117; color: #ffffff; }
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #ff9800, #f57c00);
            color: white; font-weight: bold; border-radius: 12px;
            padding: 16px; font-size: 18px; border: none;
            box-shadow: 0px 4px 10px rgba(245, 124, 0, 0.3);
        }
        .stButton>button:hover { transform: translateY(-2px); }
        .status-box {
            background-color: #1e222b; padding: 22px; border-radius: 15px;
            border-left: 5px solid #ff9800; margin-bottom: 25px;
        }
        .gm-box {
            background-color: #1a1c23; padding: 15px; border-radius: 12px;
            border: 2px dashed #00ffcc; color: #00ffcc; margin-bottom: 20px;
        }
        .clicker-box {
            background-color: #251f1a; padding: 20px; border-radius: 15px;
            border: 2px solid #ff9800; text-align: center; margin-bottom: 25px;
        }
        .msg-box {
            background-color: #161a23; padding: 20px; border-radius: 15px;
            border: 1px solid #4f5b66; margin-bottom: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🎮 잇(IT) 시대를 즐기기")
    st.markdown("#### `VIP 전용 엔드게임 사후지원 플랫폼 v1.3`")
    st.write("---")

    # 📡 [GM -> 과장님] 실시간 지령창
    current_notice = get_gm_notice()
    st.markdown(f"""
    <div class="gm-box">
        <span style='font-weight:bold;'>📡 GM(전산직 후배)의 실시간 지령:</span><br>
        <span style='font-size: 16px;'>" {current_notice} "</span>
    </div>
    """, unsafe_allow_html=True)

    # 🕹️ [영구 데이터 연동] 인싸력 강화 시스템
    player_data = load_player_data()

    st.markdown('<div class="clicker-box">', unsafe_allow_html=True)
    st.markdown("### ⚡ 잇(IT) 인싸력 강화 훈련원")
    
    # 등급 실시간 렌더링
    st.metric(label="현재 등급", value=f"Lv.{player_data['p_level']} {player_data['guild_rank']}")
    st.progress(player_data['exp'] / 100, text=f"다음 레벨업까지 EXP {player_data['exp']}%")
    
    if st.button("🔥 [인싸력 강화 주문서] 클릭하여 레벨업하기"):
        player_data['exp'] += 20
        
        # 레벨업 조건 충족 시
        if player_data['exp'] >= 100:
            player_data['p_level'] += 1
            player_data['exp'] = 0
            if player_data['p_level'] == 2: player_data['guild_rank'] = "유튜브 정복자"
            elif player_data['p_level'] == 3: player_data['guild_rank'] = "동네 스크린골프 지배자"
            elif player_data['p_level'] == 4: player_data['guild_rank'] = "자유로운 힙스터 길드장"
            else: player_data['guild_rank'] = "우주 최강 백수 마스터"
            st.balloons()
            st.toast(f"🎉 LEVEL UP! [{player_data['guild_rank']}] 달성!")
        
        # 파일에 영구 저장
        save_player_data(player_data)
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)

    # ✉️ [과장님 -> GM] 양방향 전령 발송창
    st.markdown('<div class="msg-box">', unsafe_allow_html=True)
    st.markdown("### ✉️ GM에게 전령 발송 (양방향 소통창)")
    st.write("GM(후배)에게 실시간으로 한마디를 원격 전송합니다.")
    manager_text = st.text_input("메시지 입력란:", placeholder="ex) 고맙네 후배! 훈련원 레벨 다 올렸네 하하", key="m_text")
    if st.button("🚀 전령 발송 (GM 콘솔로 전송)"):
        if manager_text:
            append_manager_message(manager_text)
            st.success("✨ 포탈을 통해 GM의 전산직 콘솔로 전령이 무사히 전달되었습니다!")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 🏆 플레이어 영구 고정 스펙 창
    st.markdown('<div class="status-box">', unsafe_allow_html=True)
    st.markdown("### 🏆 플레이어 영구 고정 스펙")
    st.markdown("**• 플레이어:** 과장님 (Level. MAX)")
    st.markdown("**• 장착 타이틀:** `신규 공무원의 등불`, `인덕(人德) 만렙`, `기다림의 미학 마스터`")
    st.markdown("**• 영구 지속 버프:** 후배 전산직의 평생 무상 IT 사후지원 항시 적용")
    st.markdown('</div>', unsafe_allow_html=True)

    # 🚨 실시간 버그 리포트
    st.markdown("## 🚨 실시간 전산 장애 버그 리포트")
    bug_type = st.selectbox("장애 증상 선택:", ["카톡이 침묵함", "유튜브 알고리즘 이상함", "와이파이 에러", "기타 디지털 버그"])
    if st.button("⚡ 긴급 GM 호출하기 (SLA 10분 보장)"):
        st.success(f"🚨 [{bug_type}] 리포트가 전담 GM에게 전송되었습니다!")

    # 🛠️ 히든 콘솔: [전산직 전용 관리자 페이지]
    st.write("---")
    with st.expander("⚙️ 시스템 관리자(전산직 후배) 전용 콘솔"):
        admin_pw = st.text_input("GM 인증 코드", type="password", key="admin_key")
        if admin_pw == "admin123":
            st.success("GM 권한 승인 완료.")
            
            # 기능 1: 과장님 화면에 지령 띄우기
            new_notice = st.text_input("과장님 앱에 띄울 실시간 메시지 입력:")
            if st.button("📡 서버 전체 공지 원격 패치 가동"):
                save_gm_notice(new_notice)
                st.success("서버 지령 업데이트 완료!")
                st.rerun()
                
            # 기능 2: 과장님이 보낸 전령(메시지) 실시간 확인하기
            st.write("---")
            st.markdown("### 📥 과장님이 보낸 전령(메시지) 목록")
            messages = get_manager_messages()
            if messages:
                for msg in messages[::-1]:  
                    st.info(msg.strip())
            else:
                st.write("아직 접수된 전령이 없습니다.")
