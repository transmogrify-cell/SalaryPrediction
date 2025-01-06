import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    ### Stack Overflow Developer Survey 2020
    """
    )

    # Enhanced Pie Chart: Data Distribution by Country using Plotly
    st.write("#### Number of Data from Different Countries")
    data = df["Country"].value_counts()

    fig1 = make_subplots(rows=1, cols=1, specs=[[{'type':'pie'}]])

    fig1.add_trace(go.Pie(labels=data.index, values=data.values, hole=0.3, 
                          hoverinfo='label+percent', textinfo='value+percent', 
                          marker=dict(colors=sns.color_palette("Set2", len(data)))))

    fig1.update_layout(title="Data Distribution by Country", title_x=0.5, title_font_size=18)

    st.plotly_chart(fig1, use_container_width=True)

    # Mean Salary Based on Country using Plotly
    st.write("#### Mean Salary Based on Country")
    country_salary = df.groupby("Country")["Salary"].mean().sort_values()

    fig2 = make_subplots(rows=1, cols=1, specs=[[{'type':'bar'}]])

    # Applying dark yellow color for the bars
    fig2.add_trace(go.Bar(x=country_salary.values, y=country_salary.index, 
                         orientation='h', marker_color='#FFD700'))

    fig2.update_layout(title="Mean Salary by Country", title_x=0.5, 
                      xaxis_title="Average Salary", yaxis_title="Country", 
                      title_font_size=18, showlegend=False)

    st.plotly_chart(fig2, use_container_width=True)

    # Mean Salary Based on Experience using Plotly
    st.write("#### Mean Salary Based on Experience")
    experience_salary = df.groupby("YearsCodePro")["Salary"].mean().sort_values()

    fig3 = make_subplots(rows=1, cols=1, specs=[[{'type':'scatter'}]])

    fig3.add_trace(go.Scatter(x=experience_salary.index, y=experience_salary.values, 
                             mode='lines+markers', line=dict(color='royalblue', width=2), 
                             marker=dict(size=8, color='red')))

    fig3.update_layout(title="Mean Salary by Years of Experience", title_x=0.5, 
                      xaxis_title="Years of Professional Experience", 
                      yaxis_title="Average Salary", title_font_size=18)

    st.plotly_chart(fig3, use_container_width=True)