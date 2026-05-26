import streamlit as st
import yfinance as yf
import google.generativeai as genai
import plotly.graph_objects as go
import pandas as pd
import time

# --- 網頁基本設定 ---
st.set_page_config(
    page_title="WallStreet AI - 華爾街級智慧股票分析系統",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 側邊欄設定 (API Key 與系統說明) ---
with st.sidebar:
    st.title("⚙️ 系統核心設定")
    st.markdown("請輸入您的 Google Gemini API Key 以啟用 AI 分析大腦。")
    
    # 讓用戶輸入 API Key (密碼隱碼形式)
    api_key = st.text_input("Gemini API Key:", type="password", help="請前往 Google AI Studio 獲取免費或付費的 API Key")
    
    if api_key:
        genai.configure(api_key=api_key)
        st.success("🤖 AI 大腦已成功連線！")
    else:
        st.warning("🔑 請輸入 API Key 以解鎖 AI 分析功能。")
        
    st.markdown("---")
    st.markdown("### 📊 系統核心模組")
    st.info(
        "1. 綜合全視角分析\n"
        "2. 5年財務數據拆解\n"
        "3. 競爭護城河評估\n"
        "4. 投行級估值模型\n"
        "5. 5-10年成長潛力\n"
        "6. 分析師多空辯論\n"
        "7. 最終投資決策建議"
    )
    st.caption("Powered by Streamlit, yfinance & Google Gemini")

# --- 主網頁標題 ---
st.title("📈 WallStreet AI 華爾街級智慧股票分析系統")
st.subheader("結合即時定量財經數據與資深分析師定性思維的 All-in-One 投資研究平台")
st.markdown("---")

# --- 用戶輸入區 ---
col_input1, col_input2 = st.columns([2, 1])
with col_input1:
    ticker = st.text_input("🔍 請輸入股票代號 (美股如: NVDA, AAPL, MSFT / 台股如: 2330.TW, 2454.TW):", "NVDA").upper().strip()

# --- 核心執行邏輯 ---
if st.button("🚀 開始執行全方位深度分析", type="primary"):
    if not api_key:
        st.error("❌ 錯誤：請先在左側邊欄輸入您的 Gemini API Key 才能啟動 AI 分析！")
    else:
        with st.spinner(f"正在連線至交易所與全球財經數據庫，擷取 {ticker} 的核心資料..."):
            try:
                # 1. 透過 yfinance 擷取真實數據
                stock = yf.Ticker(ticker)
                info = stock.info
                company_name = info.get('longName', ticker)
                current_price = info.get('currentPrice', info.get('previousClose', 'N/A'))
                currency = info.get('currency', 'USD')
                
                # 獲取財務報表
                financials = stock.financials # 損益表
                cashflow = stock.cashflow     # 現金流量表
                balance_sheet = stock.balance_sheet # 資產負債表
                hist_5y = stock.history(period="5y") # 5年股價歷史
                
                # 2. 顯示基本行情看板
                st.success(f"✅ 成功獲取 {company_name} ({ticker}) 的核心數據！")
                
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                with metric_col1:
                    st.metric("當前股價", f"{current_price} {currency}")
                with metric_col2:
                    st.metric("市值 (Market Cap)", f"{info.get('marketCap', 0):,}")
                with metric_col3:
                    st.metric("滾動本益比 (Trailing P/E)", f"{info.get('trailingPE', 'N/A')}")
                with metric_col4:
                    st.metric("遠期本益比 (Forward P/E)", f"{info.get('forwardPE', 'N/A')}")
                
                # 3. 繪製 5 年股價走勢圖 (互動式)
                st.markdown("### 📈 過去 5 年股價走勢圖")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=hist_5y.index, y=hist_5y['Close'], mode='lines', name='收盤價', line=dict(color='#0288d1', width=2)))
                fig.update_layout(
                    title=f"{company_name} 歷史價格走勢",
                    xaxis_title="日期",
                    yaxis_title=f"價格 ({currency})",
                    template="streamlit",
                    hovermode="x unified"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # 4. 整理要交給 AI 的數據文本
                # 萃取過去幾年的主要營收與淨利作為 AI 分析的參考依據
                try:
                    revenue_summary = financials.loc['Total Revenue'].to_dict() if 'Total Revenue' in financials.index else "無營收數據"
                    net_income_summary = financials.loc['Net Income'].to_dict() if 'Net Income' in financials.index else "無淨利數據"
                    fcf_summary = cashflow.loc['Free Cash Flow'].to_dict() if 'Free Cash Flow' in cashflow.index else "無自由現金流數據"
                except Exception:
                    revenue_summary = "數據格式不標準，請由 AI 自行根據市場現狀評估"
                    net_income_summary = "數據格式不標準"
                    fcf_summary = "數據格式不標準"

                                # 4. 整理要交給 AI 的數據文本 (新增技術面與基本面數據)
                try:
                    revenue_summary = financials.loc['Total Revenue'].to_dict() if 'Total Revenue' in financials.index else "無營收數據"
                    net_income_summary = financials.loc['Net Income'].to_dict() if 'Net Income' in financials.index else "無淨利數據"
                    fcf_summary = cashflow.loc['Free Cash Flow'].to_dict() if 'Free Cash Flow' in cashflow.index else "無自由現金流數據"
                except Exception:
                    revenue_summary = "數據格式不標準"
                    net_income_summary = "數據格式不標準"
                    fcf_summary = "數據格式不標準"

                # 提取技術面指標
                ma_50 = info.get('fiftyDayAverage', 'N/A')
                ma_200 = info.get('twoHundredDayAverage', 'N/A')
                high_52w = info.get('fiftyTwoWeekHigh', 'N/A')
                low_52w = info.get('fiftyTwoWeekLow', 'N/A')
                pb_ratio = info.get('priceToBook', 'N/A')
                roe = info.get('returnOnEquity', 'N/A')

                raw_data_context = f"""
                公司名稱: {company_name} ({ticker})
                當前市場數據: 當前價格={current_price}, P/E={info.get('trailingPE')}, P/B={pb_ratio}, ROE={roe}
                技術面數據: 50日均線={ma_50}, 200日均線={ma_200}, 52週最高={high_52w}, 52週最低={low_52w}
                過去幾年總營收: {revenue_summary}
                過去幾年淨利: {net_income_summary}
                過去幾年自由現金流: {fcf_summary}
                """
                
                st.markdown("---")
                st.markdown("### 🤖 華爾街 AI 分析師群報告產出")
                st.write("系統正在調度 AI 模型，針對 7 大核心模組進行解構，請稍候...")
                
                # 初始化 Gemini 模組
                          # --- 自動偵測可用模型 (解決 404 找不到模型的問題) ---
                valid_models = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        valid_models.append(m.name)
                
                # 優先挑選 flash 高速模型，若無則降級選 pro 或其他可用模型
                chosen_model = None
                for m_name in valid_models:
                    if "flash" in m_name:
                        chosen_model = m_name
                        break
                
                if not chosen_model:
                    for m_name in valid_models:
                        if "pro" in m_name:
                            chosen_model = m_name
                            break
                            
                if not chosen_model and valid_models:
                    chosen_model = valid_models[0]

                # 讓網頁顯示最終抓到哪一個模型
                st.info(f"🔍 系統自動偵測並對接 API 模型：{chosen_model}")
                
                # 正式載入偵測到的模型
                model = genai.GenerativeModel(chosen_model)
                # ----------------------------------------------------

                
                                # 建立 9 個頁籤 (Tabs)
                tabs_list = st.tabs([
                    "📋 1. 綜合全視角分析", 
                    "📈 2. 技術面分析",     # 新增
                    "💎 3. 基本面分析",     # 新增
                    "📊 4. 5年財務拆解", 
                    "🛡️ 5. 競爭護城河", 
                    "🏦 6. 投行級估值", 
                    "🚀 7. 5-10年潛力", 
                    "⚔️ 8. 分析師多空辯論", 
                    "🎯 9. 最終投資結論"
                ])
                
                # 定義 7 個強大指令
                prompts = [
                    f"以華爾街資深股票分析師的角度對 {ticker} 進行完整分析。內容包括：商業模式與收入來源、競爭優勢（護城河）、產業趨勢、財務健康狀況（營收成長、利潤率、負債）、關鍵風險、與競爭對手的估值比較、多頭/空頭與基本情境分析、未來 12–24 個月展望。請用簡單易懂的方式解釋，但保有專業分析深度。請結合以下真實數據參考：{raw_data_context}",
                    f"分析 {company_name} ({ticker}) 過去 5 年的財務數據。請詳細拆解並評論其：營收成長、淨利趨勢、自由現金流、利潤率、負債水準、股東權益報酬率（ROE）。最後必須給出明確判定：這家公司目前是財務體質正在變強，還是開始走弱。參考數據：{raw_data_context}",
                    f"評估 {company_name} 的競爭護城河。請深入分析：品牌影響力、網路效應、轉換成本、成本優勢、專利或獨家技術。並與其主要競爭對手進行比較，最後請幫這家公司的護城河強度打分（1–10 分）。",
                    f"對 {ticker} 進行估值分析（如同投資銀行研究報告）。請包含：本益比（P/E）與同業比較、折現現金流（DCF）估值邏輯、產業平均估值水準、以及該股票目前是否被低估或高估的最終結論。參考數據：{raw_data_context}",
                    f"分析 {company_name} 的未來成長潛力。請考慮：整體市場規模(TAM)、產業成長率、全球擴張機會、新產品線、AI 或最新技術優勢。並評估未來 5–10 年的潛在成長空間與天花板。",
                    f"以兩位華爾街頂尖分析師的對話方式，針對 {ticker} 進行激烈的多空辯論。一位為多頭觀點（看漲），一位為空頭觀點（看跌）。雙方都必須提出有數據或邏輯支持的扎實論點，最後請給出一個相對中性的客觀結論。參考數據：{raw_data_context}",
                    f"評估投資人是否應該投資這檔股票（股票代號：{ticker}）。請包含：短期展望（1年內）、長期展望（5年以上）、關鍵催化因素（Catalysts）、主要風險。最終給出唯一的明確操作結論：買入（Buy）、持有（Hold）或避免（Avoid）。"
                ]
                
                tabs_list = [tab1, tab2, tab3, tab4, tab5, tab6, tab7]
                
                # 依序呼叫 AI 寫入對應的分頁
                for i in range(7):
                    with tabs_list[i]:
                        with st.spinner(f"AI 正在撰寫第 {i+1} 模組報告..."):
                            response = model.generate_content(prompts[i])
                            st.markdown(response.text)
                            time.sleep(1) # 稍微緩衝避免 API 頻率限制
                            
                st.balloons() # 分析完成發送慶祝氣球
                
            except Exception as e:
                st.error(f"❌ 分析過程中發生錯誤。可能原因：輸入的股票代號有誤、該公司數據未公開、或 API Key 異常。錯誤訊息：{e}")