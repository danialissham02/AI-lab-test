import json
from typing import List, Dict, Any, Tuple
import operator
import streamlit as st

# ============================ #
# 1) RULE ENGINE CONFIGURATION #
# ============================ #
COMPARISONS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
}

DEFAULT_CONDITIONS: List[Dict[str, Any]] = [
    {
        "rule_name": "Windows open → turn off AC",
        "rule_priority": 100,
        "trigger_conditions": [["windows_open", "==", True]],
        "ac_action": {
            "mode": "OFF",
            "fan_speed": "LOW",
            "setpoint": None,
            "reason": "Windows are open"
        }
    },
    {
        "rule_name": "No one home → eco mode",
        "rule_priority": 90,
        "trigger_conditions": [
            ["occupancy", "==", "EMPTY"],
            ["temperature", ">=", 24]
        ],
        "ac_action": {
            "mode": "ECO",
            "fan_speed": "LOW",
            "setpoint": 27,
            "reason": "Home empty, save energy"
        }
    },
    {
        "rule_name": "Hot & humid (occupied) → strong cooling",
        "rule_priority": 80,
        "trigger_conditions": [
            ["occupancy", "==", "OCCUPIED"],
            ["temperature", ">=", 30],
            ["humidity", ">=", 70]
        ],
        "ac_action": {
            "mode": "COOL",
            "fan_speed": "HIGH",
            "setpoint": 23,
            "reason": "Hot and humid"
        }
    },
    {
        "rule_name": "Hot (occupied) → cool",
        "rule_priority": 70,
        "trigger_conditions": [
            ["occupancy", "==", "OCCUPIED"],
            ["temperature", ">=", 28]
        ],
        "ac_action": {
            "mode": "COOL",
            "fan_speed": "MEDIUM",
            "setpoint": 24,
            "reason": "Temperature high"
        }
    },
    {
        "rule_name": "Slightly warm (occupied) → gentle cool",
        "rule_priority": 60,
        "trigger_conditions": [
            ["occupancy", "==", "OCCUPIED"],
            ["temperature", ">=", 26],
            ["temperature", "<", 28]
        ],
        "ac_action": {
            "mode": "COOL",
            "fan_speed": "LOW",
            "setpoint": 25,
            "reason": "Slightly warm"
        }
    },
    {
        "rule_name": "Night (occupied) → sleep mode",
        "rule_priority": 75,
        "trigger_conditions": [
            ["occupancy", "==", "OCCUPIED"],
            ["time_of_day", "==", "NIGHT"],
            ["temperature", ">=", 26]
        ],
        "ac_action": {
            "mode": "SLEEP",
            "fan_speed": "LOW",
            "setpoint": 26,
            "reason": "Night comfort"
        }
    },
    {
        "rule_name": "Too cold → turn off AC",
        "rule_priority": 85,
        "trigger_conditions": [["temperature", "<=", 22]],
        "ac_action": {
            "mode": "OFF",
            "fan_speed": "LOW",
            "setpoint": None,
            "reason": "Already cold"
        }
    }
]

def validate_condition(facts: Dict[str, Any], condition: List[Any]) -> bool:
    field, op, value = condition
    if field not in facts or op not in COMPARISONS:
        return False
    return COMPARISONS[op](facts[field], value)

def check_rule_match(facts: Dict[str, Any], rule: Dict[str, Any]) -> bool:
    return all(validate_condition(facts, cond) for cond in rule["trigger_conditions"])

def execute_rules(facts: Dict[str, Any], rules: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    triggered_rules = [rule for rule in rules if check_rule_match(facts, rule)]
    if not triggered_rules:
        return {"mode": "OFF", "reason": "No matching rules"}, []
    
    sorted_rules = sorted(triggered_rules, key=lambda r: r["rule_priority"], reverse=True)
    return sorted_rules[0]["ac_action"], sorted_rules

# ============================== #
# 2) REDESIGNED INTERFACE UI    #
# ============================== #
st.set_page_config(page_title="AC Controller Pro", layout="wide")

# Updated CSS: Removed fixed white backgrounds to support Dark Mode
st.markdown("""
    <style>
    /* Use transparent backgrounds with borders so they adapt to theme */
    div[data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 15px;
        border-radius: 10px;
    }
    .status-card {
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #007bff;
        background-color: rgba(128, 128, 128, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("❄️ ClimateControl AI Dashboard")
st.markdown("---")

col_in, col_out = st.columns([1, 1], gap="large")

with col_in:
    st.subheader("📍 Environment Sensors")
    temp = st.slider("Ambient Temperature (°C)", 10, 45, 22)
    humid = st.slider("Relative Humidity (%)", 0, 100, 46)
    
    st.markdown("---")
    st.subheader("🏠 Home State")
    occ = st.radio("Occupancy Status", ["OCCUPIED", "EMPTY"], horizontal=True)
    tod = st.radio("Current Period", ["DAY", "NIGHT"], horizontal=True)
    win = st.toggle("Windows / Ventilation Open", value=False)
    
    run_btn = st.button("Apply Settings & Sync AC", use_container_width=True, type="primary")

facts_data = {
    "temperature": temp,
    "humidity": humid,
    "occupancy": occ,
    "time_of_day": tod,
    "windows_open": win
}

with col_out:
    if run_btn:
        action, matched = execute_rules(facts_data, DEFAULT_CONDITIONS)
        
        st.subheader("🕹️ System Output")
        
        # Display as high-level metrics
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Mode", action['mode'])
        with m2: st.metric("Fan", action['fan_speed'])
        with m3: st.metric("Target", f"{action['setpoint']}°C" if action['setpoint'] else "N/A")
        
        # Using built-in containers that handle theme colors automatically
        with st.container(border=True):
            st.markdown(f"**Decision Logic:** {action['reason']}")
        
        with st.expander("View Logic Trace"):
            st.write("### Sensor Data Snapshot")
            st.json(facts_data)
            
            st.write("### Rule Processing Queue")
            if matched:
                for i, r in enumerate(matched):
                    symbol = "✅" if i == 0 else "📎"
                    st.write(f"{symbol} **{r['rule_name']}**")
                    st.caption(f"Priority Score: {r['rule_priority']}")
            else:
                st.warning("No logic rules triggered. System defaulting to OFF.")
    else:
        st.info("Adjust the sensors on the left and click **Apply Settings** to simulate the AC logic.")

st.markdown("---")
st.caption("ClimateControl AI v2.0 • Rule-Based Expert System")
