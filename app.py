# app.py
import streamlit as st
from planner.agent import generate_plan
from planner.db import save_plan, get_all_plans
import json

st.set_page_config(page_title="🧠 AI Task Planner", layout="wide")
st.title("🧠 AI Task Planner")

goal = st.text_input("Enter a new goal ")

col1, col2, col3 = st.columns(3)
with col1:
    enter_clicked = st.button("📝 Enter Goal")
with col2:
    generate_clicked = st.button("⚙️ View Generated Plan")
with col3:
    history_clicked = st.button("📜 Browse Previous Plans")

if enter_clicked:
    if goal:
        st.success("✅ Goal entered. Now click 'View Generated Plan' to generate your itinerary.")
    else:
        st.warning("⚠️ Please enter a goal first.")

if generate_clicked:
    if goal:
        with st.spinner("Generating plan..."):
            plan = generate_plan(goal)
            save_plan(goal, plan)
        st.success("✅ Plan generated successfully!")
        st.markdown("---")
        st.header("📅 Your Generated Plan")

        for day in plan:
            st.subheader(f"📆 Day {day['day']}")
            st.write(f"**Task**: {day['task']}")

            # ✅ Handle places gracefully
            if day.get("places"):
                st.write("**Places:**")
                for place in day["places"]:
                    st.markdown(f"- {place}")
            else:
                st.info("ℹ️ No specific places for this plan.")

            # ✅ Weather still shown for context
            if day.get("weather"):
                st.write(f"**Weather**: 🌤️ {day['weather']}")

    else:
        st.warning("⚠️ Please enter a goal before generating.")

if history_clicked:
    st.markdown("---")
    st.header("📜 Plan History")
    history = get_all_plans()
    if history:
        for h in history:
            st.markdown(f"**🕒 {h[2]}** — _{h[0]}_")
            try:
                # h[1] is stored as str(plan), so try parsing back
                plan_data = json.loads(h[1].replace("'", '"'))
                st.code(json.dumps(plan_data, indent=2, ensure_ascii=False), language="json")
            except Exception:
                st.code(str(h[1]))
    else:
        st.info("No plans saved yet.")
