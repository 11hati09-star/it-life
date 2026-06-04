import streamlit as st

# 모바일 화면 최적화 설정
st.set_page_config(
    page_title="잇(IT) 시대를 즐기기",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# MMORPG 감성의 다크 테마 커스텀 CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ff9800, #f57c00);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 16px;
        font-size: 18px;
        border: none;
        box-shadow: 0px 4px 10px rgba(245, 124, 0, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 15px rgba(245, 124, 0, 0.5);
    }
    .status-box {
        background-color: #1e222b;
        padding: 22px;
        border-radius: 15px;
        border-left: 5px solid #ff9800;
        margin-bottom: 25px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
    }
    .content-box {
        background-color: #161a23;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2d3139;
        margin-bottom: 12px;
    }
    .patch-box {
        background-color: #1c202a;
        padding: 15px;
        border-radius: 10px;
        border-bottom: 2px solid #4f5b66;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------
# TITLE & HEADER
# -----------------------------------------------------------------
st.title("🎮 잇(IT) 시대를 즐기기")
st.markdown("#### `VIP 전용 엔드게임 사후지원 플랫폼 v1.0`")
st.write("---")

# -----------------------------------------------------------------
# 1. 플레이어 캐릭터 정보창 (Status)
# -----------------------------------------------------------------
st.markdown('<div class="status-box">', unsafe_allow_html=True)
st.markdown("### 🏆 만렙 플레이어 스테이터스")
st.markdown("**• 플레이어:** 과장님 (Level. MAX)")
st.markdown("**• 클래스:** 영예로운 퇴직자 (공직 마스터)")
st.markdown("**• 전 소속 길드:** 동해 오피스 ➡️ **[현 소속]** 자유주의 힙스터 길드")
st.markdown("**• 장착 타이틀:** `신규 공무원의 등불`, `인덕(人德) 만렙`, `기다림의 미학 마스터`")
st.markdown("**• 영구 버프:** 후배 전산직의 평생 무상 IT 사후지원 항시 적용")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------
# 2. 엔드게임 콘텐츠: '잇(it)' 라이프 가이드
# -----------------------------------------------------------------
st.markdown("## 🧭 잇(it) 라이프 핵심 가이드")
st.write("이제 출근 전쟁은 끝났습니다. 전산직 후배가 보증하는 스마트 디지털 콘텐츠를 즐기세요.")

with st.expander("📺 광고 없이 유튜브/OTT 즐기는 팁"):
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("**1. 유튜브 프리미엄 활용하기**\n- 광고 없이 트로트, 골프, 옛날 예능 영상을 끊김 없이 보실 수 있는 필수 버프입니다.")
    st.markdown("**2. 스마트 TV 연동**\n- 스마트폰 화면을 거실 큰 TV로 미러링하여 영화관처럼 즐기는 방법을 세팅해 드립니다.")
    st.markdown('</div>', unsafe_allow_html=True)

with st.expander("📸 스마트폰 인생샷 사진첩 마스터"):
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("- 등산이나 여행 가셔서 풍경 사진 기가 막히게 찍는 기본 구도 팁 가이드 수록 예정.")
    st.markdown("- 터치 한 번으로 얼굴 화사하게 나오는 추천 보정 앱 패치 예정.")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------
# 3. 핵심 기능: 실시간 버그 리포트 (SLA 핫라인)
# -----------------------------------------------------------------
st.write("---")
st.markdown("## 🚨 실시간 전산 장애 버그 리포트")
st.write("디지털 세상(스마트폰, PC, 와이파이 등)에서 버그가 발생하면 즉시 전담 GM을 호출하세요.")

bug_type = st.selectbox(
    "현재 발생한 장애 증상을 선택하세요:",
    ["카카오톡이 알 수 없는 이유로 침묵함", 
     "유튜브 알고리즘이 이상한 영상만 추천함", 
     "와이파이 비밀번호가 기억의 저편으로 사라짐", 
     "기타 디지털 세상의 모든 짜증나는 에러"]
)

# 호출 버튼 클릭 시 이벤트
if st.button("⚡ 긴급 GM 호출하기 (SLA 10분 보장)"):
    st.balloons()
    st.success(f"🚨 [{bug_type}] 버그 리포트가 전담 GM에게 실시간으로 접수되었습니다!")
    st.info("💡 과장님, 실제로 연락을 주시면 GM이 원격 및 출장 버그 수정을 즉시 지원합니다.")

# -----------------------------------------------------------------
# 4. 지속 가능성의 핵심: 패치 노트 (Patch Notes)
# -----------------------------------------------------------------
st.write("---")
st.markdown("## 📢 전담 GM 정기 패치 노트")

st.markdown('<div class="patch-box">', unsafe_allow_html=True)
st.markdown("#### 🛠️ Ver 1.0.0 (그랜드 오픈) - 2026.06.05")
st.markdown("- 과장님의 영예로운 정년퇴직 기념 대시보드 서버 정식 오픈")
st.markdown("- 평생 무상 전산 AS 핫라인 상시 가동")
st.markdown("- 실수 가득했던 신규 공무원을 믿고 기다려주신 것에 대한 **'무한 감사 버프'** 상시 적용")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="patch-box">', unsafe_allow_html=True)
st.markdown("#### ⏳ Ver 1.1.0 (명절 시즌 패치 예정)")
st.markdown("- 추석 맞이 극성 스팸 메시지 차단 및 필터링 시스템 업데이트")
st.markdown("- 단체 안부 문자 터치 한 번으로 보내기 매크로 가이드 탑재 예정")
st.markdown('</div>', unsafe_allow_html=True)

st.info("🔒 본 앱은 과장님 전용 VIP 플랫폼입니다. 삭제하지 마시면 주기적으로 새로운 꿀팁과 기능이 원격 패치됩니다!")