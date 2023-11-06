import inspect
import textwrap

import streamlit as st

from demo_echarts import ST_DEMOS
from demo_pyecharts import ST_PY_DEMOS
from streamlit_echarts import JsCode
from streamlit_echarts import st_echarts
import pandas as pd



def main():
    st.title("California Racial Justice Act")
    df = pd.read_excel('data/RJAsheet1.xlsx')
    df['2023_Case Load'] = df['2023_Case Load'].astype(int)
    df['2023_Foreign Born Releases'] = df['2023_Foreign Born Releases'].astype(int)
    df['2024_Case Load'] = df['2024_Case Load'].astype(int)
    df['2024_In Custody'] = df['2024_In Custody'].astype(int)
    df['2025_Case Load'] = df['2025_Case Load'].astype(int)
    df['Felony Convictions 2015-2023'] = df['Felony Convictions 2015-2023'].astype(int)
    st.divider()
    
    with st.sidebar:
        toggle = ('Graphs','Maps')
        
        toggle_result = st.selectbox(
            label="Select Type",
            options=toggle,
        )
        county_options = ('Orange','Alameda', 'Alpine*', 'Amador', 'Butte', 'Calaveras', 'Colusa*', 'Contra Costa', 'Del Norte', 'El Dorado', 'Fresno', 'Glenn*', 'Humboldt', 'Imperial', 'Inyo', 'Kern', 'Kings', 'Lake', 'Lassen', 'Los Angeles*', 'Madera', 'Marin', 'Mariposa', 'Mendocino', 'Merced', 'Modoc', 'Mono', 'Monterey', 'Napa*', 'Nevada', 'Placer', 'Plumas', 'Riverside', 'Sacramento*', 'San Benito', 'San Bernardino*', 'San Diego*', 'San Francisco*', 'San Joaquin', 'San Luis Obispo', 'San Mateo', 'Santa Barbara', 'Santa Clara', 'Santa Cruz', 'Shasta', 'Sierra', 'Siskiyou', 'Solano', 'Sonoma*', 'Stanislaus', 'Sutter', 'Tehama', 'Trinity', 'Tulare', 'Tuolumne', 'Ventura', 'Yolo', 'Yuba')
        selected_county = st.selectbox(
            label="Select County",
            options=county_options,
        )
        percentage_options = (100,90,80,70,60,50,40,30,20,10)

        percentage = st.selectbox(
            label="Percentage of Eligible Offenders who utilize RJA",
            options=percentage_options,
        )
        st.markdown('''# RJA Relief Eligibility Dashboard

This dashboard projects the number of defendants likely to be eligible for relief under the charging and sentencing disparity provisions of the RJA (Penal Code section 745, subdivisions (a)(3)-(4)).

## How to Use the Dashboard:

1. Select the county of interest.
2. Select the utilization percentage.

The utilization percentage is an estimate of the proportion of defendants eligible under the RJA who will actually choose to file a claim. As this number is entirely unknown currently, you may wish to experiment with different rates to see the overall impact.
''')
    if toggle_result == 'Graphs':
        df1 = df[df['County'] == selected_county]
        st.subheader("Projected case load for " + selected_county + " county while " + str(percentage) + " Percentage of Eligible Offenders utilize RJA")
        st.divider()
        options = {
            "tooltip": {"trigger": "item", "axisPointer": {"type": "shadow"}, "order" : "valueDesc"},
            "legend": {"type" : "plain", "top" : 2,
                       "textStyle": {"fontSize" : 18, 'color' : 'white' }
                      },
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            "xAxis": {},
            "yAxis": {
                "axisLabel" : {
                     "fontWeight" : "bolder",
                     "fontSize" : 18,
                    "color": "white"
                },
                "data": ["2023","2024","2025"]
            },
            
            
            "series": [
                {
                    "name": "Annual Eligible Caseload",
                    "type": "bar",
                    "stack": "total",
                    "label": {
                        "show": True,
                        "position" : "bottom",
                        "color" : "white"
                             },
                    "data": [(df1['2023_Case Load'].iloc[0] * percentage /100),(df1['2024_Case Load'].iloc[0] * percentage /100),(df1['2025_Case Load'].iloc[0] * percentage /100)],
                },
                {
                    "name": "Foreign Born Prison Releases",
                    "type": "bar",
                    "stack": "total",
                    "label": {
                        "show": True,
                        "position" : "bottom",
                        "color" : "white"
                             },
                    "data": [(df1['2023_Foreign Born Releases'].iloc[0] * percentage /100),None,None],
                },
    
    
                {
                    "name": "Eligible in Custody",
                    "type": "bar",
                    "stack": "total",
                    "label": {
                        "show": True,
                        "position" : "bottom",
                        "color" : "white"
                             },
                    "data": [
                        None,
                        df1['2024_In Custody'].iloc[0] * percentage /100,
                        None
                    ],
                },
    
                {
                    "name": "Felony Convictions 2015 - 2022",
                    "type": "bar",
                    "stack": "total",
                    "label": {
                        "show": True,
                        "position" : "bottom",
                        "color" : "white"
                             },
                    "data": [None,None,df1['Felony Convictions 2015-2023'].iloc[0] * percentage /100],
                },
            ],
        }
        st_echarts(options=options, height="500px")
        st.markdown('''
# Metrics Description
1. **Total Non-White Caseload**
   - Description: Caseload is calculated as the total number of 2022 felony petitions filed in the county that are not filed against White defendants. The number assumes that most RJA petitions will come from felony cases.

2. **Foreign-Born Non-White Inmates Scheduled for Release in 2023**
   - Description: The number of Foreign-Born Inmates released by county is not known. The number is calculated from the 2021 total CDCR released population, multiplied by the percent of the state-wide in-custody population that is foreign-born, adjusted for the percent of the state’s foreign-born population that resides in each county. This makes several assumptions. It assumes that each county incarcerates foreign-born residents at the same rate, which is likely not true. It also assumes that all foreign-born inmates have immigration consequences that may result from their arrest. This also assumes that the foreign-born population is as likely to be released as the native-born population. Overall, the number is very inaccurate, but it is also very small. As such, the impact of the inaccuracy on the overall trend is minuscule.

3. **Non-White In-Custody Population**
   - Description: The number of non-White CDCR inmates by county is not known. The population is estimated by estimating each county’s in-custody population and adjusting by the state-wide non-White in-custody proportion. It assumes that each county incarcerates non-white residents at the same rate, which is likely not true. Generally, if California county-driven incarceration follows patterns of racial disparity found in scientific studies, then counties with smaller non-White populations will likely have a higher rate of non-White incarceration. The estimates also do not account for inmates serving felony sentences in county jails. Data on these populations are not readily calculable, but since such sentences will be shorter, the ability of county jail inmates to file petitions prior to release, based on cases that became final without an RJA motion being filed, is expected to be more limited than the capacity of CDCR inmates to file petitions.

4. **Non-White Felony Convictions 2015-2023**
   - Description: Race of felony convictions is not known, so total felony convictions from each county are multiplied by the percentage of felony arrests within each county that are non-White. This is likely an underestimate, as the number of felony arrests is significantly smaller than the number of felony convictions, but if any bias exists within any part of the arrest-to-conviction pipeline, then non-White convictions will outpace non-White arrests. 2023 numbers are imputed from 2022. White foreign-born defendants will generally not make RJA claims (though they may be eligible under the statute).

5. **Note on Condemned Death-Row Population**
   - Description: I choose not to include the current condemned death-row population, largely because (outside of Los Angeles County) this is a very small population at the county level. Since the L.A. district attorney pledged to reduce all death sentences to life without parole, but has not yet done so, it was not readily clear how best to classify these cases.

6. **Note on Total Felony Convictions**
    - Description: Total felony convictions are not known for these counties. Convictions are calculated by adjusting total felony petitions by the state-wide rate of felony conviction for counties that report petitions.

# Data Sources

1. **Felony Petitions**
   - Source: Arrest disposition data file, California Attorney General
   - [Data Link](https://openjustice.doj.ca.gov/data)

2. **County-level Race and Citizenship**
   - Source: American Community Survey, 5-Year Small Area Estimates, U.S. Census Bureau.

3. **In-Custody Incarcerated Population**
   - Source: Offender Data Points, Release and In-Custody Data Sources, California Department of Corrections and Rehabilitation
   - [Data Link](https://public.tableau.com/app/profile/cdcr.or/viz/OffenderDataPoints/SummaryInCustodyandParole)

4. **Total Convictions**
   - Source: Court Statistics Report Statewide Caseload Trends, 2014–15 to 2021–22, published by the Judicial Council of California
   - [Data Link](https://www.courts.ca.gov/13421.htm)

''')
    elif toggle_result == 'Maps':
        pass
       
if __name__ == "__main__":
    st.set_page_config(
        page_title="RJA", page_icon=":chart_with_upwards_trend:"
    )
    main()
    
