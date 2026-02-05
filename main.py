import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import data

# main.py
# --------------------------------------------------------------
# This is the frontend layer of the application, implemented using Streamlit.
# It utilizes the MissionData class from data.py to fetch and display data.

try:
    missionData = data.MissionData("space_missions.csv")

    companyFrame = sorted(missionData.csv["Company"].unique())
    locationFrame = sorted(missionData.csv["Location"].unique())
    rocketFrame = sorted(missionData.csv["Rocket"].unique())

    missionFrame = sorted(missionData.csv["Mission"].unique())
    rocketStatusFrame = sorted(missionData.csv["RocketStatus"].unique())
    missionStatusFrame = sorted(missionData.csv["MissionStatus"].unique())


    st.set_page_config(layout="wide")
    st.markdown("# :red[Space Missions Dashboard]", text_alignment="center")

    st.divider()

    # SUMMARY STATISTICS SECTION
    # ---------------------------------------------------------------
    st.markdown("## :red[*Summary Statistics*]", text_alignment="center")
    
    colA, colB, colC = st.columns(3)

    with colA:
        totalMissions = len(missionData.csv)
        st.metric("Total Missions", totalMissions)

    with colB:
        successCount = len(missionData.csv[missionData.csv["MissionStatus"] == "Success"])
        successRate = (successCount / totalMissions * 100)
        st.metric("Success Rate", f"{successRate:.2f}%")

    with colC:
        totalCompanies = missionData.totalCompanies
        st.metric("Total Companies", totalCompanies)

    colD, colE, colF = st.columns(3)
    
    with colD:
        mostActiveCompany = missionData.getTopCompaniesByMissionCount(1)[0]
        st.metric("Most Active Company", mostActiveCompany[0], delta=f"{mostActiveCompany[1]} missions")

    with colE:
        totalRockets = missionData.csv["Rocket"].nunique()
        st.metric("Total Rockets", totalRockets)
    
    with colF:
        mostUsedRocket = missionData.getMostUsedRocket()
        rocketUses = len(missionData.csv[missionData.csv["Rocket"] == mostUsedRocket])
        st.metric("Most Used Rocket", mostUsedRocket, delta=f"{rocketUses} missions")

    st.divider()

    # VISUALS SECTION
    # ---------------------------------------------------------------
    st.markdown("## :red[*Visuals*]", text_alignment="center")

    # Success Rate by Company Bar Chart
    companySuccesses = []
    for company in companyFrame:
        missionCount = missionData.getMissionCountByCompany(company)
        successRate = missionData.getSuccessRate(company)
        
        companySuccesses.append({
            "Company": company,
            "Success Rate": successRate,
            "Mission Count": missionCount
        })

    companySuccessFrame = pd.DataFrame(companySuccesses)

    companySuccessFrame = companySuccessFrame.sort_values("Mission Count", ascending=False)

    figA = px.bar(
        companySuccessFrame,
        x="Company",
        y="Success Rate",
        title="Success Rate by Company (Sorted by Total Missions)",
        labels={
            "Success Rate": "Success Rate (%)",
            "Company": "Company Name"
        },
        hover_data={
            "Mission Count": True,
            "Success Rate": ":.1f"
        }
    )

    figA.update_traces(marker_color="rgba(0, 0, 255, 0.65)")

    figA.update_xaxes(tickangle=-45)

    figA.update_layout(
        xaxis_title="Company",
        yaxis_title="Success Rate (%)",
        yaxis_range=[0, 100]
    )

    st.plotly_chart(figA, use_container_width=True)

    # Line Plot for Missions and Success Rate Over Time
    yearlyMissionsAndSuccesses = []

    for year in range(missionData.minYear, missionData.maxYear + 1):
        yearlyMissions = missionData.csv[missionData.csv["Date"].dt.year == year]
        totalMissions = len(yearlyMissions)

        if totalMissions > 0:
            successes = len(yearlyMissions[yearlyMissions["MissionStatus"] == "Success"])
            success_rate = (successes / totalMissions) * 100
        else:
            success_rate = 0

        yearlyMissionsAndSuccesses.append({
            "Year": year,
            "Total Missions": totalMissions,
            "Success Rate": round(success_rate, 2)
        })

    yearlyMissionsAndSuccessesFrame = pd.DataFrame(yearlyMissionsAndSuccesses)

    figB = go.Figure()

    figB.add_trace(
        go.Scatter(
            x=yearlyMissionsAndSuccessesFrame["Year"],
            y=yearlyMissionsAndSuccessesFrame["Total Missions"],
            name="Total Missions",
            mode="lines+markers"
        )
    )

    figB.add_trace(
        go.Scatter(
            x=yearlyMissionsAndSuccessesFrame["Year"],
            y=yearlyMissionsAndSuccessesFrame["Success Rate"],
            name="Success Rate (%)",
            mode="lines+markers",
            yaxis="y2"
        )
    )

    figB.update_layout(
        title="Total Missions and Success Rate Over Time",
        xaxis_title="Year",
        yaxis=dict(
            title="Total Missions"
        ),
        yaxis2=dict(
            title="Success Rate (%)",
            overlaying="y",
            side="right",
            range=[0, 100]
        ),
        hovermode="x unified"
    )

    st.plotly_chart(figB, use_container_width=True)

    # Rocket Reliability Heat Map
    rocketStatusCounts = (
        missionData.csv
        .groupby(["Rocket", "MissionStatus"])
        .size()
        .reset_index(name="Count")
    )

    figC = px.density_heatmap(
        rocketStatusCounts,
        x="Rocket",
        y="MissionStatus",
        z="Count",
        color_continuous_scale="Reds",
        title="Rocket Reliability Heatmap",
        labels={
            "Rocket": "Rocket",
            "MissionStatus": "Mission Outcome",
            "Count": "Number of Missions"
        }
    )

    figC.update_layout(
        xaxis_tickangle=-45,
        yaxis_title="Mission Status",
        xaxis_title="Rocket",
        coloraxis_colorbar=dict(
            title="Missions"
        )
    )

    figC.update_traces(
        hovertemplate=
        "<b>Rocket:</b> %{x}<br>" +
        "<b>Status:</b> %{y}<br>" +
        "<b>Missions:</b> %{z}<extra></extra>"
    )

    st.plotly_chart(figC, use_container_width=True)

    st.divider()

    # FILTER AND DATA TABLE SECTION
    # ---------------------------------------------------------------
    st.markdown("## :red[*Table View*]", text_alignment="center")

    col1, col2, col3 = st.columns(3)

    with col1:
        company = st.multiselect(
            "Filter by Company:",
            companyFrame,
            placeholder="Select a company..."
        )

    with col2:
        location = st.multiselect(
            "Filter by Location:",
            locationFrame,
            placeholder="Select a location..."
        )

    with col3:
        rocket = st.multiselect(
            "Filter by Rocket:",
            rocketFrame,
            placeholder="Select a rocket..."
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        mission = st.multiselect(
            "Filter by Mission:",
            missionFrame,
            placeholder="Select a mission..."
        )

    with col5:
        rocketStatus = st.selectbox(
            "Filter by Rocket Status:",
            rocketStatusFrame,
            index=None,
            placeholder="Select a rocket status..."
        )

    with col6:
        missionStatus = st.multiselect(
            "Filter by Mission Status:",
            missionStatusFrame,
            placeholder="Select a mission status..."
        )

    year_range = st.slider(
        "Filter by Year Range:",
        min_value=missionData.minYear,
        max_value=missionData.maxYear,
        value=(missionData.minYear, missionData.maxYear),
        step=1
    )

    if company == [] and location == [] and rocket == [] and mission == [] and rocketStatus is None and missionStatus == [] and year_range == (missionData.minYear, missionData.maxYear):
        st.dataframe(missionData.csv)
    else:
        filteredMissions = missionData.csv.copy()

        if company and company != []:
            filteredMissions = filteredMissions[filteredMissions["Company"].isin(company)]

        if location and location != []:
            filteredMissions = filteredMissions[filteredMissions["Location"].isin(location)]

        if rocket and rocket != []:
            filteredMissions = filteredMissions[filteredMissions["Rocket"].isin(rocket)]

        if mission and mission != []:
            filteredMissions = filteredMissions[filteredMissions["Mission"].isin(mission)]

        if rocketStatus is not None:
            filteredMissions = filteredMissions[filteredMissions["RocketStatus"] == rocketStatus]

        if missionStatus and missionStatus != []:
            filteredMissions = filteredMissions[filteredMissions["MissionStatus"].isin(missionStatus)]

        filteredMissions = filteredMissions[(filteredMissions["Date"].dt.year >= year_range[0]) & (filteredMissions["Date"].dt.year <= year_range[1])]

        st.dataframe(filteredMissions)
except:
    st.markdown("# :red[There was an error loading the data. Please try again.]", text_alignment="center")

