import streamlit as st
import os
import json
from datetime import datetime

# 모바일 화면 최적화 및 메타 설정 (v0.014)
st.set_page_config(
    page_title="it 시대를 즐기기",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------
# 💾 서버 영구 저장 및 로그 시스템 (DB 레이어 구축)
# -----------------------------------------------------------------
NOTICE_FILE = "gm_notice.txt"
MSG_FILE = "manager_messages.txt"
SAVE_FILE = "player_save.json"
LOG_FILE = "system_log.txt"

# 직급 딕셔너리 (국가 전산직 공무원 테크트리)
def get_rank_name(level):
    ranks = {
        1: "전산서기보 (9급)",
        2: "전산서기 (8급)",
        3: "전산주사보 (7급)",
        4: "전산주사 (6급)",
        5: "전산사무관 (5급)",
        6: "전산서기관 (44급)",
        7: "전산부이사관 (3급)",
        8: "전산이사관 (2급)",
        9: "전산관리관 (1급)"
    }
    return ranks.get(level, "전산대통령 (👑)")

# 시스템 실시간 로그 기록 함수
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
            # 하위 호환성 및 신규 필드 방어코드
            if "last_access" not in data: data["last_access"] = "기록 없음"
            return data
    return {"exp": 0, "p_level": 1, "guild_rank": "전산서기보 (9급)", "last_access": "기록 없음"}

def save_player_data(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# -----------------------------------------------------------------
# 🛡️ 소스코드 카피 방지 스크립트
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
# 🔑 가상 라우팅 시스템 (접속 코드 검증)
# -----------------------------------------------------------------
if "user_role" not in st.session_state:
    st.session_state.user_role = None

if st.session_state.user_role is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("🔒 잇(IT) 시대를 즐기기")
    st.subheader("보안 시스템 검증 단계")
    st.write("지정된 자산 액세스 코드를 입력하여 시스템을 가동하세요.")

    user_password = st.text_input("액세스 코드 입력", type="password", placeholder="코드를 입력하세요")
    
    if st.button("인증 메커니즘 가동"):
        if user_password == "qkrdudcjf": 
            st.session_state.user_role = "player"
            # 로그인 성공 시 최근접속일 업데이트 및 로그 기록
            p_data = load_player_data()
            p_data["last_access"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_player_data(p_data)
            append_log("시스템 접속", "과장님이 성공적으로 인증을 마치고 대시보드에 진입했습니다.")
            st.rerun()
        elif user_password == "admin123":
            st.session_state.user_role = "admin"
            append_log("관리자 접속", "GM강현이 제어 콘솔에 접근했습니다.")
            st.rerun()
        else:
            st.error("❌ 접근 권한이 없습니다. 지정된 자산 코드가 아닙니다.")

# -----------------------------------------------------------------
# 🕹️ [USER PAGE] 과장님 전용 런처 레이어
# -----------------------------------------------------------------
elif st.session_state.user_role == "player":
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
    st.markdown("#### `VIP 전용 엔드게임 사후지원 플랫폼 v0.014`")
    st.write("---")

    # GM 실시간 지령 피드
    current_notice = get_gm_notice()
    st.markdown(f"""
    <div class="gm-box">
        <span style='font-weight:bold;'>📡 GM강현의 실시간 지령:</span><br>
        <span style='font-size: 16px;'>" {current_notice} "</span>
    </div>
    """, unsafe_allow_html=True)

    # 훈련원 구역 (게이지 바 정렬 및 레이아웃 수정)
    player_data = load_player_data()
    st.markdown('<div class="clicker-box">', unsafe_allow_html=True)
    st.markdown("### ⚡ 디지털 라이프 적응력 강화 훈련원")
    
    st.metric(label="현재 직급 레벨", value=f"Lv.{player_data['p_level']} {player_data['guild_rank']}")
    # 게이지 바가 다른 버튼과 꼬이지 않도록 명확하게 훈련원 박스 안에 격리
    st.progress(player_data['exp'] / 100, text=f"다음 직급 승진까지 진척도 {player_data['exp']}%")
    
    if st.button("🔥 [적응력 주문서] 클릭하여 기술 연마하기"):
        player_data['exp'] += 20
        append_log("행동 훈련", f"과장님이 훈련원 버튼을 클릭했습니다. (EXP: {player_data['exp']-20}% -> {player_data['exp']}%)")
        
        if player_data['exp'] >= 100:
            player_data['p_level'] += 1
            player_data['exp'] = 0
            player_data['guild_rank'] = get_rank_name(player_data['p_level'])
            st.balloons()
            st.toast(f"🎉 승진 축하드립니다! [{player_data['guild_rank']}] 달성!")
            append_log("직급 승진", f"과장님이 Lv.{player_data['p_level']} [{player_data['guild_rank']}]에 도달하셨습니다!")
        
        save_player_data(player_data)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 양방향 전령 시스템 (예시 안내 문구 삭제)
    st.markdown('<div class="msg-box">', unsafe_allow_html=True)
    st.markdown("### ✉️ GM에게 전령 발송 (양방향 소통창)")
    st.write("GM강현에게 메시지를 원격 전송합니다.")
    manager_text = st.text_input("메시지 입력란:", placeholder="", key="m_text")
    if st.button("🚀 전령 발송 (GM 콘솔로 전송)"):
        if manager_text:
            append_manager_message(manager_text)
            append_log("전령 수신", f"과장님이 전령을 발송했습니다: '{manager_text}'")
            st.success("✨ 포탈을 통해 GM강현의 전산직 콘솔로 전령이 무사히 전달되었습니다!")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 스테이터스 및 고정 스펙
    st.markdown('<div class="status-box">', unsafe_allow_html=True)
    st.markdown("### 🏆 플레이어 영구 고정 스펙")
    st.markdown("**• 플레이어:** 과장님 (Level. MAX)")
    st.markdown("**• 장착 타이틀:** `신규 공무원의 등불`, `인덕(人德) 만렙`, `기다림의 미학 마스터`")
    st.markdown("**• 영구 지속 버프:** GM강현의 평생 무상 IT 사후지원 항시 적용")
    st.markdown('</div>', unsafe_allow_html=True)

    # 전산 장애 리포트
    st.markdown("## 🚨 실시간 전산 장애 버그 리포트")
    bug_type = st.selectbox("장애 증상 선택:", ["카톡이 침묵함", "유튜브 알고리즘 이상함", "와이파이 에러", "기타 디지털 버그"])
    if st.button("⚡ 긴급 GM 호출하기 (SLA 10분 보장)"):
        st.success(f"🚨 [{bug_type}] 리포트가 전담 GM에게 전송되었습니다!")
        append_log("장애 접수", f"과장님이 [{bug_type}] 긴급 호출을 발동하셨습니다.")

    st.write("---")
    if st.button("🚪 시스템 안전 로그아웃"):
        append_log("세션 종료", "과장님이 안전하게 로그아웃하셨습니다.")
        st.session_state.user_role = None
        st.rerun()

# -----------------------------------------------------------------
# 🛠️ [ADMIN PAGE] GM강현 전용 제어 및 라이브 모니터링 레이어
# -----------------------------------------------------------------
elif st.session_state.user_role == "admin":
    st.markdown("""
        <style>
        .main { background-color: #0b0f19; color: #ffffff; }
        .stat-display { background-color: #161b26; padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #233554; }
        .patch-btn>button { background: linear-gradient(135deg, #00ffcc, #00b3ff) !important; color: #0b0f19 !important; }
        .log-display { background-color: #070a14; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 13px; color: #a2b1cd; max-height: 25px; overflow-y: scroll; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🛠️ GM강현 전용 제어 콘솔")
    st.markdown("#### `서버 백엔드 및 실시간 모니터링 시스템`")
    st.write("---")

    # 과장님 라이브 스탯 현황판 + 최근접속일 추적
    player_data = load_player_data()
    st.markdown("<div class='stat-display'>", unsafe_allow_html=True)
    st.markdown("### 📊 라이브 플레이어(과장님) 계정 상태")
    st.write(f"• **최근 시스템 접속 일시:** `{player_data['last_access']}`")
    st.write(f"• **현재 직급:** {player_data['guild_rank']} (Lv.{player_data['p_level']})")
    st.write(f"• **강화 진척도:** {player_data['exp']}%")
    st.markdown("</div>", unsafe_allow_html=True)

    # 🔧 미세조정 관리자 커스텀 툴
    st.subheader("⚙️ 플레이어 스탯 미세조정 변조기")
    set_lv = st.number_input("레벨 강제 변조 (1-10):", min_value=1, max_value=10, value=int(player_data['p_level']))
    set_exp = st.slider("EXP 진척도 강제 조정 (%):", min_value=0, max_value=80, step=20, value=int(player_data['exp']))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 위 설정값으로 과장님 계정 변조"):
            player_data['p_level'] = set_lv
            player_data['exp'] = set_exp
            player_data['guild_rank'] = get_rank_name(set_lv)
            save_player_data(player_data)
            append_log("스탯 변조", f"GM강현이 계정 데이터를 강제 수정했습니다. (Lv.{set_lv}, EXP {set_exp}%)")
            st.success("스탯 원격 변조 완료!")
            st.rerun()
    with col2:
        if st.button("🚨 [초기화] 계정 데이터 완전 리셋"):
            init_data = {"exp": 0, "p_level": 1, "guild_rank": "전산서기보 (9급)", "last_access": "데이터 리셋됨"}
            save_player_data(init_data)
            append_log("데이터 초기화", "GM강현이 과장님의 세이브 파일을 서버 초기 상태로 완전 리셋했습니다.")
            st.warning("과장님의 계정이 9급 서기보 원점으로 초기화되었습니다.")
            st.rerun()

    st.write("---")

    # 실시간 공지 원격 배포
    st.subheader("📡 서버 실시간 공지 원격 패치")
    new_notice = st.text_input("과장님 화면 상단에 실시간으로 심어줄 메시지 입력:")
    st.markdown('<div class="patch-btn">', unsafe_allow_html=True)
    if st.button("📡 원격 실시간 공지사항 배포 가동"):
        save_gm_notice(new_notice)
        append_log("공지 배포", f"GM공지가 업데이트되었습니다: '{new_notice}'")
        st.success("서버 동기화 성공! 과장님 메인 화면에 즉시 적용되었습니다.")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    
    # 실시간 로그 모니터링 시스템 수록
    st.subheader("📜 블랙박스 시스템 라이브 로그")
    logs = get_logs()
    log_text = "".join(logs[::-1])  # 최신 로그가 맨 위에 표시되도록 역순 정렬
    st.text_area("서버 액티비티 로그", value=log_text, height=180, disabled=True)

    st.write("---")
    
    # 과장님 수신 전령 목록
    st.subheader("📥 과장님이 보낸 전령(메시지) 보관소")
    messages = get_manager_messages()
    if messages:
        for msg in messages[::-1]:  
            st.info(msg.strip())
    else:
        st.write("아직 서버로 수신된 전령이 없습니다.")

    st.write("---")
    if st.button("🚪 GM 세션 안전 종료"):
        st.session_state.user_role = None
        st.rerun()
