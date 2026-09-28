import streamlit as st
import pandas as pd
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Streamlit 요소 갤러리',
    page_icon='🧩',
    layout='wide',
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    # - GDP for 1962
    # - ...
    # - GDP for 2022
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GDP
    #
    # So let's pivot all those year-columns into two: Year and GDP
    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )

    # Convert years from string to integers
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df

gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Draw the example gallery and the original GDP dashboard.

st.title('🧩 Streamlit 요소 갤러리')
st.caption('텍스트부터 데이터 시각화까지, 웹 앱을 구성하는 요소를 직접 조작해 보세요.')

gallery_tab, dashboard_tab = st.tabs(['요소 둘러보기', 'GDP 대시보드'])

with gallery_tab:
    basics_tab, data_tab = st.tabs(['입력과 피드백', '데이터와 레이아웃'])

    with basics_tab:
        st.header('텍스트와 안내')
        st.markdown('''
        Streamlit 앱은 **Python 코드 몇 줄**로 인터랙티브한 웹 화면을 만듭니다.
        제목, 본문, 링크, 코드 블록 같은 콘텐츠를 자연스럽게 배치할 수 있어요.
        ''')
        st.code("st.title('안녕하세요, Streamlit!')\nst.button('눌러 보기')", language='python')

        message_cols = st.columns(4)
        message_cols[0].success('성공 메시지')
        message_cols[1].info('정보 메시지')
        message_cols[2].warning('주의 메시지')
        message_cols[3].error('오류 메시지')

        st.divider()
        st.header('입력 위젯')
        left_col, right_col = st.columns(2)

        with left_col:
            visitor_name = st.text_input('이름', placeholder='예: 민지')
            favorite_topic = st.selectbox('관심 주제', ['데이터 분석', '머신러닝', '웹 앱'])
            favorite_tools = st.multiselect(
                '사용해 본 도구', ['Pandas', 'Plotly', 'Altair', 'SQL'],
                default=['Pandas'],
            )
            chart_style = st.radio('선호하는 차트', ['선 그래프', '막대 그래프'], horizontal=True)

        with right_col:
            detail_level = st.slider('표시할 상세도', min_value=1, max_value=10, value=6)
            sample_count = st.number_input('샘플 개수', min_value=1, max_value=100, value=12)
            show_details = st.toggle('상세 정보 표시', value=True)
            subscribe = st.checkbox('새 예제 알림 받기')
            visit_date = st.date_input('방문 날짜')
            visit_time = st.time_input('방문 시간')

        if visitor_name:
            st.write(f'{visitor_name}님은 **{favorite_topic}** 주제에 관심이 있군요.')
        st.caption(
            f'선택한 도구: {", ".join(favorite_tools) or "없음"} · '
            f'상세도 {detail_level}/10 · {sample_count}개 · '
            f'{visit_date} {visit_time} · 알림 {"켜짐" if subscribe else "꺼짐"}'
        )
        if show_details:
            st.write(f'차트 유형: {chart_style}')

        with st.form('feedback_form'):
            st.subheader('폼과 제출 버튼')
            feedback = st.text_area('한 줄 의견', placeholder='어떤 요소가 가장 유용했나요?')
            submitted = st.form_submit_button('의견 제출', type='primary')
        if submitted:
            st.success(f'의견을 확인했어요: {feedback or "내용 없음"}')

        button_col, toast_col = st.columns(2)
        with button_col:
            if st.button('풍선 효과 보기', icon='🎈'):
                st.balloons()
        with toast_col:
            if st.button('토스트 알림 보기', icon='🔔'):
                st.toast('작은 알림도 간단하게 띄울 수 있어요.')

        with st.expander('접고 펼치는 설명'):
            st.write('`st.expander` 안에 긴 설명이나 선택적인 세부 정보를 담을 수 있습니다.')

    with data_tab:
        st.header('지표와 표')
        metric_cols = st.columns(3)
        metric_cols[0].metric('방문자', '1,284', '+12%')
        metric_cols[1].metric('평균 체류 시간', '4분 32초', '+18초')
        metric_cols[2].metric('오류율', '0.4%', '-0.2%', delta_color='inverse')

        sample_df = pd.DataFrame({
            '월': ['1월', '2월', '3월', '4월', '5월', '6월'],
            '방문자': [120, 148, 135, 190, 224, 260],
            '만족도': [4.1, 4.3, 4.2, 4.5, 4.6, 4.8],
        })
        st.subheader('편집 가능한 데이터')
        edited_df = st.data_editor(
            sample_df,
            num_rows='dynamic',
            width='stretch',
            hide_index=True,
        )
        if chart_style == '선 그래프':
            st.line_chart(edited_df, x='월', y='방문자')
        else:
            st.bar_chart(edited_df, x='월', y='방문자')

        csv_data = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            'CSV 다운로드',
            data=csv_data,
            file_name='streamlit-demo.csv',
            mime='text/csv',
            icon='⬇️',
        )

        st.subheader('파일 업로드')
        uploaded_file = st.file_uploader('CSV 파일을 선택하세요', type=['csv'])
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file)
                st.dataframe(uploaded_df, width='stretch')
            except Exception as error:
                st.error(f'CSV를 읽지 못했습니다: {error}')

        with st.container(border=True):
            st.write('**레이아웃 컨테이너**')
            st.caption('열, 탭, 확장 영역, 컨테이너를 조합해 정보를 정돈할 수 있습니다.')

with dashboard_tab:
    st.title('🌍 GDP 대시보드')
    st.markdown('World Bank Open Data의 국가별 GDP를 연도에 따라 비교합니다.')

    min_value = gdp_df['Year'].min()
    max_value = gdp_df['Year'].max()

    from_year, to_year = st.slider(
        '조회 연도',
        min_value=min_value,
        max_value=max_value,
        value=[min_value, max_value],
    )

    countries = gdp_df['Country Code'].unique()
    selected_countries = st.multiselect(
        '비교할 국가',
        countries,
        ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'],
    )

    filtered_gdp_df = gdp_df[
        (gdp_df['Country Code'].isin(selected_countries))
        & (gdp_df['Year'] <= to_year)
        & (from_year <= gdp_df['Year'])
    ]

    st.header('연도별 GDP', divider='gray')
    st.line_chart(filtered_gdp_df, x='Year', y='GDP', color='Country Code')

    last_year = gdp_df[gdp_df['Year'] == to_year]
    st.header(f'{to_year}년 GDP', divider='gray')
    metric_cols = st.columns(4)
    for index, country in enumerate(selected_countries):
        country_rows = last_year[last_year['Country Code'] == country]['GDP'].dropna()
        if country_rows.empty:
            continue
        value = country_rows.iloc[0] / 1_000_000_000
        metric_cols[index % len(metric_cols)].metric(
            label=f'{country} GDP',
            value=f'{value:,.0f}B',
        )
