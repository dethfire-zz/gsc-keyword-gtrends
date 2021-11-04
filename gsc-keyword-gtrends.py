import streamlit as st
import pandas as pd
import json
import requests
import time
from pytrends.request import TrendReq

st.markdown("""
<style>
.big-font {
    font-size:50px !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<p class="big-font">Google Trends in GSC Keywordsr</p>
<b>Directions: </b></ br><ol>
<li>Export Performance data (impressions, CTR, positon) in Google Search Console. Upload Queries.csv from the zip file.</li>
""", unsafe_allow_html=True)

cutoff = st.number_input('Number of queries', min_value=1, max_value=100, value=10)
pause = st.number_input('Pause between calls', min_value=1, max_value=5, value=2)
timeframe = st.selectbox('Timeframe',('1-m', '3-m', '12-m'))

geo = st.selectbox('Geo',('Worldwide', 'US'))

if geo == 'Wordwide':
    geo = ''

get_gsc_file = st.file_uploader("Upload GSC CSV File",type=['csv'])  

if get_gsc_file is not None:
    st.write("Data upload success, processing... :sunglasses:")
    
    df = pd.read_csv(get_gsc_file, encoding='utf-8')
    df.sort_values(by=['Impressions'], ascending=False, inplace=True)
    #df.drop([0,3], inplace=True)
    df = df[:cutoff]
    
    d = {'Keyword': [], 'Trend': []}
    df3 = pd.DataFrame(data=d)
    keywords = []
    trends = []

    for index, row in df.iterrows():
      keyword = row['Top queries']
      pytrends = TrendReq(hl='en-US', tz=360)
      kw_list = [keyword]
      pytrends.build_payload(kw_list, cat=0, timeframe='today '+timeframe, geo=geo, gprop='')
      df2 = pytrends.interest_over_time()
      keywords.append(keyword)
      try:

        trend1 = int((df2[keyword][-5] + df2[keyword][-4] + df2[keyword][-4])/3)
        trend2 = int((df2[keyword][-4] + df2[keyword][-3] + df2[keyword][-2])/3)
        trend3 = int((df2[keyword][-3] + df2[keyword][-2] + df2[keyword][-1])/3)

        print(trend1)
        print(trend2)
        print(trend3)

        if trend3 > trend2 and trend2 > trend1:
          print(keyword + " is trending up")
          trends.append('UP')
        elif trend3 < trend2 and trend2 < trend1:
          print(keyword + " is trending down")
          trends.append('DOWN')
        else:
          print(keyword + " is flat")
          trends.append('FLAT')
      except:
        print(keyword + " has no data")
        trends.append('N/A')
      time.sleep(pause)
      
    df3['Keyword'] = keywords
    df3['Trend'] = trends
    st.dataframe(df3)      

st.write('Author: [Greg Bernhardt](https://twitter.com/GregBernhardt4) | Friends: [importSEM](https://www.importsem.com) and [Physics Forums](https://www.physicsforums.com)')
