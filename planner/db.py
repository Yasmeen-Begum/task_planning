# planner/db.py
import sqlite3
import json

conn = sqlite3.connect("plans.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal TEXT,
    plan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def save_plan(goal, plan):
    # store plan as JSON string for better fidelity
    plan_json = json.dumps(plan, ensure_ascii=False)
    cursor.execute("INSERT INTO plans (goal, plan) VALUES (?, ?)", (goal, plan_json))
    conn.commit()

def get_all_plans():
    cursor.execute("SELECT goal, plan, created_at FROM plans ORDER BY created_at DESC")
    rows = cursor.fetchall()
    # convert plan column back to python structure for nicer UI usage
    out = []
    for goal, plan_json, created_at in rows:
        try:
            plan_obj = json.loads(plan_json)
        except:
            plan_obj = plan_json
        out.append((goal, plan_obj, created_at))
    return out
