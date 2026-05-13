import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt # 👈 시각화 라이브러리 추가
import seaborn as sns           # 👈 고급 시각화 라이브러리 추가
from datetime import datetime
import os

# 한글 폰트 설정 (리눅스 서버 환경용 설정은 나중에 로컬에서 더 자세히 다룰게요!)
# 일단은 기본적인 그래프 생성 로직에 집중합니다.

def collect_g7_financial_data():
    print(f"작업 시작 시간: {datetime.now()}")

    # [1~3단계 동일: 데이터 수집 및 데이터프레임 변환 로직]
    g7_conf = {
        '미국': {'index': '^GSPC', 'fx': 'USDKRW=X'},
        '일본': {'index': '^N225', 'fx': 'JPYKRW=X'},
        '영국': {'index': '^FTSE', 'fx': 'GBPKRW=X'},
        '캐나다': {'index': '^GSPTSE', 'fx': 'CADKRW=X'},
        '독일': {'index': '^GDAXI', 'fx': 'EURKRW=X'},
        '프랑스': {'index': '^FCHI', 'fx': 'EURKRW=X'},
        '이탈리아': {'index': 'FTSEMIB.MI', 'fx': 'EURKRW=X'}
    }
    data_list = []
    for country, tickers in g7_conf.items():
        try:
            idx = yf.Ticker(tickers['index']).history(period='1d')['Close'].iloc[-1]
            fx = yf.Ticker(tickers['fx']).history(period='1d')['Close'].iloc[-1]
            data_list.append({
                '날짜': datetime.now().strftime('%Y-%m-%d'),
                '국가': country,
                '주가지수': round(idx, 2),
                '환율(KRW)': round(fx, 2)
            })
        except Exception as e:
            print(f"{country} 데이터 수집 중 오류: {e}")

    df_new = pd.DataFrame(data_list)
    file_name = 'G7_Economic_Data.xlsx'
    
    # 4. 데이터 통합 저장
    if not os.path.exists(file_name):
        df_final = df_new
    else:
        df_existing = pd.read_excel(file_name)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    
    df_final.to_excel(file_name, index=False)
    print(f"데이터 저장 완료: {file_name}")

    # 🚀 5. 자동 시각화 (새로 추가된 '화가' 기능)
    try:
        # 최근 30일 데이터만 시각화 (데이터가 너무 많아지면 지저분하니까요!)
        plt.figure(figsize=(12, 6))
        sns.set_style("whitegrid")
        
        # 국가별 환율 추이 그래프 그리기
        plot = sns.lineplot(data=df_final, x='날짜', y='환율(KRW)', hue='국가', marker='o')
        plt.title('G7 Exchange Rate Trend (KRW)', fontsize=15)
        plt.xticks(rotation=45) # 날짜 겹침 방지
        
        # 그래프를 이미지 파일로 저장
        plt.tight_layout()
        plt.savefig('G7_Exchange_Chart.png') 
        print("그래프 시각화 완료: G7_Exchange_Chart.png")
    except Exception as e:
        print(f"시각화 중 오류 발생: {e}")

collect_g7_financial_data()
