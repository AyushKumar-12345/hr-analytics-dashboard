# --- FIX: FULL CIRCULAR DONUT CHART ---
with c1:
    st.markdown("""
    <div class="panel-container">
        <div class="panel-title">Attrition Proportion</div>
        <div class="panel-caption">Active headcount vs departed personnel</div>
    """, unsafe_allow_html=True)

    att_counts = filtered["Attrition"].value_counts().reset_index()
    att_counts.columns = ["Attrition", "Count"]

    fig_donut = px.pie(
        att_counts,
        names="Attrition",
        values="Count",
        hole=0.68,
        color="Attrition",
        color_discrete_map={"No": "#00E5FF", "Yes": "#FF6D00"}
    )
    fig_donut.update_traces(
        textposition="outside",
        textinfo="percent+label",
        textfont=dict(color="#D1D5DB", size=11),
        marker=dict(line=dict(color="#0B0F19", width=2.5)),
        pull=[0.02, 0.02]
    )
    fig_donut.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(t=30, b=30, l=30, r=30)
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# --- FIX: VISIBLE DEPARTMENT BARS WITH LABELS ---
with c2:
    st.markdown("""
    <div class="panel-container">
        <div class="panel-title">Attrition Rate by Department</div>
        <div class="panel-caption">Turnover concentration across organizational business units</div>
    """, unsafe_allow_html=True)

    dept_group = (
        filtered.groupby("Department")["Attrition"]
        .apply(lambda s: (s == "Yes").mean() * 100)
        .round(1)
        .reset_index(name="AttritionRate")
    )

    fig_dept = px.bar(
        dept_group,
        x="Department",
        y="AttritionRate",
        color_discrete_sequence=["#FF6D00"],
        text="AttritionRate"
    )
    fig_dept.update_traces(
        texttemplate="%{text}%",
        textposition="outside",
        textfont=dict(color="#FFFFFF", size=12)
    )
    fig_dept.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8"),
        height=320,
        margin=dict(t=30, b=40, l=55, r=15),
        xaxis=dict(showgrid=False, linecolor="rgba(255,255,255,0.1)", tickfont=dict(color="#FFFFFF")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", linecolor="rgba(255,255,255,0.1)", ticksuffix="%")
    )
    st.plotly_chart(fig_dept, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)
