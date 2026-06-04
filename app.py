import streamlit as st
import os
import json
from datetime import datetime

# 모바일 화면 최적화 및 메타 설정 (v0.022 UI 클린업)
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
    .stButton>button:hover { transform: translateY(-2px); }
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
    ranks = {
        1: "전산서기보 (9급) [전산실 막내]",
        2: "전산서기 (8급) [행정망 해결사]",
        3: "전산주사보 (7급) [과기정통부 AI 주무관]",
        4: "전산주사 (6급) [디지털보안팀장]",
        5: "전산사무관 (5급) [SW정책과 차석]",
        6: "전산서기관 (4급) [디지털정부기획과장]",
        7: "전산부이사관 (3급) [디지털플랫폼정부위원회 위원회 본부장]",
        8: "전산이사관 (2급) [국가정보자원관리원장]",
        9: "전산관리관 (1급) [과기정통부 실장 / 국가 CTO]",
        10: "디지털플랫폼정부위원회 위원장 (차관급)",
        11: "과학기술정보통신부 장관 (장관급)",
        12: "기획재정부 장관 겸 경제부총리 (부총리급)",
        13: "대한민국 국무총리 (행정부 2인자)",
        14: "대한민국 대통령 (👑 디지털 혁신 대통령)"
    }
    return ranks.get(level, "👑 대한민국 대통령 (👑 디지털 혁신 대통령)")

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
            
            if data.get("p_level", 1) > 14:
                data["p_level"] = 14
                data["guild_rank"] = get_rank_name(14)
                data["exp"] = 100
            return data
    return {"exp": 0, "p_level": 1, "guild_rank": "전산서기보 (9급) [전산실 막내]", "last_access": "기록 없음"}

def save_player_data(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

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
    st.markdown("#### `VIP 전용 엔드게임 사후지원 플랫폼 v0.022`")
    st.write("---")

    current_notice = get_gm_notice()
    st.markdown(f"""
    <div class="gm-box">
        <span style='font-weight:bold;'>📡 GM강현의 실시간 지령:</span><br>
        <span style='font-size: 16px;'>" {current_notice} "</span>
    </div>
    """, unsafe_allow_html=True)

    player_data = load_player_data()
    
    st.markdown("### ⚡ 국가 디지털 혁신 능력 강화 훈련원")
    st.metric(label="현재 관직 스펙", value=f"Lv.{player_data['p_level']} {player_data['guild_rank']}")
    st.progress(player_data['exp'] / 100, text=f"다음 랭크 상위 승진까지 진척도 {player_data['exp']}%")
    st.write("") # 약간의 여백
    
    if st.button("🔥 [적응력 주문서] 클릭하여 행정 역량 강화하기"):
        if player_data['p_level'] >= 14:
            if player_data['exp'] < 100:
                player_data['exp'] += 20
                if player_data['exp'] > 100:
                    player_data['exp'] = 100
                append_log("행동 훈련", f"과장님이 최고 직급 상태에서 최종 역량을 연마했습니다. (EXP: {player_data['exp']}%)")
            else:
                st.toast("👑 이미 최고 정점인 '대한민국 대통령' 단계에 완벽하게 도달하셨습니다!")
        else:
            player_data['exp'] += 20
            append_log("행동 훈련", f"과장님이 역량 강화 훈련을 실행했습니다. (EXP: {player_data['exp']-20}% -> {player_data['exp']}%)")
            
            if player_data['exp'] >= 100:
                player_data['p_level'] += 1
                player_data['exp'] = 0
                player_data['guild_rank'] = get_rank_name(player_data['p_level'])
                st.balloons()
                st.toast(f"🎉 초고속 영전! [{player_data['guild_rank']}] 직급에 취임하셨습니다!")
                append_log("직급 승진", f"과장님이 Lv.{player_data['p_level']} [{player_data['guild_rank']}] 레벨에 올랐습니다.")
        
        save_player_data(player_data)
        st.rerun()

    st.write("---")

    with st.expander("🚀 '디지털 혁신 대통령' 전체 커리어 로드맵 도감 확인"):
        st.markdown("""
        **[1단계] 실무 기술 전문가 과정 (9급 ~ 6급)**
        * **Lv.1 9급 전산서기보:** 전산실 막내 / 국가 시스템 모니터링 및 실무 보조
        * **Lv.2 8급 전산서기:** 정부 행정망 유지보수 / 국가적 전산 장애 직접 해결하며 두각
        * **Lv.3 7급 전산주사보:** 과기정통부 인공지능기반과 주무관 / 정부 AI 도입 초기 프로젝트 전담
        * **Lv.4 6급 전산주사:** 과기정통부 디지털보안팀장 / 국가 핵심 보안 시스템 국산화 성공

        **[2단계] 디지털 정책 관리자 과정 (5급 ~ 4급)**
        * **Lv.5 5급 전산사무관:** 과기정통부 소프트웨어정책과 차석 / 전 국민 대상 디지털 서비스 기획
        * **Lv.6 4급 전산서기관:** 디지털정부기획과장 / 정부 부처 최초 'AI 행정망' 구축 주도

        **[3단계] 고위공무원단 및 최고기술책임자(CTO) 과정 (3급 ~ 1급)**
        * **Lv.7 3급 전산부이사관:** 디지털플랫폼정부위원회 위원회 본부장 / 전 부처 데이터를 하나로 잇는 초거대 플랫폼 설계
        * **Lv.8 2급 전산이사관:** 국가정보자원관리원장 / 국가 클라우드 센터 총괄 및 사이버 테러 방어 사령탑
        * **Lv.9 1급 전산관리관:** 과기정통부 정보화정책실장 / 대한민국 기술직 공무원의 정점이자 '국가 CTO'

        **[4단계] 국가 디지털 사령탑 (차관급 ~ 부총리급 정무직)**
        * **Lv.10 차관급 위원장:** 디지털플랫폼정부위원회 위원장 / 행정 전체의 디지털 대전환 진두지휘
        * **Lv.11 장관급 장관:** 과학기술정보통신부 장관 / 대한민국을 세계 1위 'AI·디지털 패권국'으로 선도
        * **Lv.12 경제부총리:** 기획재정부 장관 겸 경제부총리 / 기술과 경제를 결합한 '디지털 노믹스' 정책 가동

        **[5단계] 행정부 권력의 정점 (국무총리 ~ 대통령)**
        * **Lv.13 국무총리:** 행정부 2인자로서 범정부 차원의 국가 위기 관리 및 디지털 융합 정책 총괄
        * **Lv.14 대한민국 대통령:** 전산직 9급 출신 최초의 국가원수 / '기술 강국 대한민국'을 완성하는 혁신 대통령
        """)

    st.write("---")

    st.markdown("### ✉ Preserved 전령 발송 (GM 소통창)")
    st.write("GM강현의 제어 콘솔로 실시간 비공개 전령을 전송합니다.")
    manager_text = st.text_input("메시지 입력란:", placeholder="", key="m_text")
    if st.button("🚀 전령 발송하기"):
        if manager_text:
            append_manager_message(manager_text)
            append_log("전령 수신", f"과장님이 전령을 발송했습니다: '{manager_text}'")
            st.success("✨ 서버 포탈을 통해 GM강현의 전산직 관리자 콘솔로 전령이 도달했습니다!")
            st.rerun()
            
    st.write("---")

    # 빈 껍데기 박스 없이 텍스트를 하나의 박스 안에 깔끔하게 통합 렌더링
    st.markdown("""
    <div class="status-box">
        <h3 style='margin-top: 0;'>🏆 플레이어 고정 패시브 스펙</h3>
        <b>• 플레이어:</b> 조규동 과장님 (Level. MAX)<br><br>
        <b>• 영구 장착 타이틀:</b> <code style='color:#ff9800;'>신규 공무원의 등불</code>, <code style='color:#ff9800;'>인덕(人德) 만렙</code>, <code style='color:#ff9800;'>기다림의 미학 마스터</code><br><br>
        <b>• 상시 적용 버프:</b> GM강현의 평생 무상 전산 장애 사후지원 프로토콜
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🚨 실시간 전산 장애 버그 리포트")
    bug_type = st.selectbox("장애 증상 선택:", ["카톡이 침묵함", "유튜브 알고리즘 이상함", "와이파이 에러", "기타 디지털 버그"])
    if st.button("⚡ 긴급 GM 호출하기 (SLA 10분 보장)"):
        st.success(f"🚨 [{bug_type}] 리포트가 전담 GM에게 전송되었습니다!")
        append_log("장애 접수", f"과장님이 [{bug_type}] 긴급 기술 지원을 호출하셨습니다.")

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

    player_data = load_player_data()
    
    # 어드민 페이지 매트릭스도 단일 박스로 통합하여 클린업
    st.markdown(f"""
    <div class='stat-display'>
        <h3 style='margin-top:0;'>📊 실시간 플레이어(과장님) 계정 매트릭스</h3>
        • <b>최근 대시보드 로그인 타임스탬프:</b> <code style='color:#00ffcc;'>{player_data['last_access']}</code><br><br>
        • <b>현재 원격 직급 상태:</b> {player_data['guild_rank']} (Lv.{player_data['p_level']})<br><br>
        • <b>현재 랭크 경험치 진척도:</b> {player_data['exp']}%
    </div>
    """, unsafe_allow_html=True)

    st.subheader("⚙️ 서버 레벨 및 스탯 강제 변조기")
    set_lv = st.number_input("대권 관직 강제 변조 (Lv.1 - Lv.14):", min_value=1, max_value=14, value=int(player_data['p_level']))
    set_exp = st.slider("승진 경험치 강제 할당 (%):", min_value=0, max_value=100, step=20, value=int(player_data['exp']))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 입력한 밸런싱 값으로 서버 변조"):
            player_data['p_level'] = set_lv
            player_data['exp'] = set_exp
            player_data['guild_rank'] = get_rank_name(set_lv)
            save_player_data(player_data)
            append_log("스탯 변조", f"GM강현이 계정 데이터를 원격 변조했습니다. (Lv.{set_lv}, EXP {set_exp}%)")
            st.success("데이터 강제 주입 성공!")
            st.rerun()
    with col2:
        if st.button("🚨 서버 세이브 데이터 공장 초기화"):
            init_data = {"exp": 0, "p_level": 1, "guild_rank": "전산서기보 (9급) [전산실 막내]", "last_access": "데이터 리셋 완료"}
            save_player_data(init_data)
            append_log("데이터 초기화", "GM강현이 과장님의 세이브 파일을 초기 9급 공무원 상태로 포맷했습니다.")
            st.warning("서버의 모든 데이터가 초기화되어 9급 서기보 막내 상태로 리셋되었습니다.")
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
