"""
Nutrition Exchange Dashboard - Streamlit App
Built around ExchangeAppBackend from meal_plan_tracking.py
Run with: streamlit run nutrition_dashboard.py
"""

import streamlit as st
import pandas as pd
from fractions import Fraction
import uuid

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nutrition Tracker",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Core layout */
    .block-container { padding: 1rem 1rem 3rem; max-width: 480px; }

    /* Hide Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }

    /* Category card */
    .cat-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 14px 16px 10px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid var(--accent);
    }
    .cat-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 6px;
    }
    .cat-name { font-weight: 700; font-size: 15px; color: #1a1a2e; }
    .cat-count { font-size: 13px; color: #555; }
    .cat-remaining { font-size: 11px; color: #888; margin-top: 4px; }

    /* Progress bar wrapper */
    .prog-track {
        background: #f0f0f0;
        border-radius: 8px;
        height: 10px;
        overflow: hidden;
        margin-top: 6px;
    }
    .prog-fill {
        height: 100%;
        border-radius: 8px;
        transition: width 0.4s ease;
        background: var(--accent);
    }

    /* Badge chip */
    .badge {
        display: inline-block;
        font-size: 10px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 20px;
        margin-left: 6px;
    }
    .badge-done  { background: #d4edda; color: #155724; }
    .badge-over  { background: #f8d7da; color: #721c24; }
    .badge-going { background: #e8f4fd; color: #0c5460; }

    /* Log form card */
    .form-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 18px 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        margin-bottom: 16px;
    }

    /* Section heading */
    .section-title {
        font-size: 18px;
        font-weight: 800;
        color: #1a1a2e;
        margin: 20px 0 12px;
    }

    /* Meal history table */
    .hist-row {
        display: flex;
        justify-content: space-between;
        padding: 7px 0;
        border-bottom: 1px solid #f2f2f2;
        font-size: 13px;
    }
    .hist-item { color: #222; font-weight: 500; }
    .hist-meta { color: #888; font-size: 11px; }

    /* Streamlit tweaks */
    div[data-testid="stSelectbox"] > div { border-radius: 10px !important; }
    div[data-testid="stNumberInput"] input { border-radius: 10px !important; }
    button[kind="primary"] { border-radius: 12px !important; font-weight: 700 !important; }
    div[data-testid="stSuccess"] { border-radius: 12px; }
    div[data-testid="stWarning"] { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ── Colour palette per category ───────────────────────────────────────────────
CAT_COLORS = {
    "Protein":    "#4361ee",
    "Cereals":    "#f4a261",
    "Fats":       "#e76f51",
    "Fruits":     "#2a9d8f",
    "Vegetables": "#57cc99",
    "Dairy":      "#9b5de5",
}
CAT_ICONS = {
    "Protein": "🥩", "Cereals": "🌾", "Fats": "🥑",
    "Fruits": "🍎", "Vegetables": "🥦", "Dairy": "🥛",
}

# ── Embedded data (mirrors meal_plan_tracking.py) ─────────────────────────────
RAW_DATA = {
    "Protein": [
        ("Beef Steak","30","g"),("Flank Steak","30","g"),("Fresh Tuna","30","g"),
        ("Fresh Cod","45","g"),("Fresh Squid","45","g"),("Chicken Breast","35","g"),
        ("Salmon","35","g"),("Medium Shrimp","5","pcs"),("Pacotilla Shrimp","6","pcs"),
        ("Turkey Ham","2","slices"),("Whole Egg","1","pc"),("Egg Whites","2","pcs"),
        ("Panela Cheese","40","g"),("Mozzarella Cheese","30","g"),("Oaxaca Cheese","30","g"),
        ("Tofu","40","g"),("Beans","1/2","cup"),("Lentils","1/2","cup"),
        ("Chickpeas","1/2","cup"),("Protein Powder","17","g"),
    ],
    "Cereals": [
        ("Cooked Rice","1/3","cup"),("Cooked Pasta","1/2","cup"),("Quinoa","1/3","cup"),
        ("Oat Flakes","1/2","cup"),("Cooked Sweet Potato","1/3","cup"),
        ("Cooked Potato","1/2","pc"),("Corn Tortilla","1","pc"),("Salmas","2","pcs"),
        ("Dehydrated Toast","2","pcs"),("Popcorn","2.5","cups"),
    ],
    "Fats": [
        ("Avocado","1/3","pc"),("Olive Oil","1","tbsp"),("Vegetable Oil","1","tbsp"),
        ("Almonds","10","pcs"),("Walnuts","3","pcs"),("Peanuts","14","pcs"),
        ("Peanut Butter","1.5","tbsp"),("Chia Seeds","1","tbsp"),("Shredded Coconut","2","tbsp"),
    ],
    "Fruits": [
        ("Apple","1","pc"),("Banana","1/2","pc"),("Blueberries","3/4","cup"),
        ("Blackberries","1","cup"),("Coconut Water","1.5","cups"),
        ("Fresh Cranberry","1.5","cups"),("Fresh Cherries","20","pcs"),
        ("Red Plum","2","pcs"),("Prune","7","pcs"),("Date","2","pcs"),
        ("Raspberry","1","cup"),("Strawberries","1","cup"),("Passion Fruit","3","pcs"),
        ("Gooseberries","1","cup"),("Guava","3","pcs"),("Pink Guava","1","pc"),
        ("Fig","2","pcs"),("Kiwi","2","pcs"),("Lychees","12","pcs"),("Mango","1/2","pc"),
        ("Melon","1","cup"),("Mixed Berries","3/4","cup"),("Papaya","1","cup"),
        ("Raisins","10","pcs"),("Pear","1/2","pc"),("Pineapple","3/4","cup"),
        ("Dragon Fruit","2","pcs"),("Rambutan","7","pcs"),("Watermelon","1","cup"),
        ("Prickly Pears","2","pcs"),("Grapes","1","cup"),("Peach","2","pcs"),
        ("Lime","3","pcs"),("Tangerine","2","pcs"),("Orange","2","pcs"),("Grapefruit","1","pc"),
    ],
    "Vegetables": [
        ("Celery","1/2","cup"),("Artichoke","1/2","cup"),("Eggplant","1/2","cup"),
        ("Onion","1/2","cup"),("Tomato","1/2","cup"),("Zucchini","1/2","cup"),
        ("Mushrooms","1/2","cup"),("Broccoli","1/2","cup"),("Cauliflower","1/2","cup"),
        ("Peas","1/2","cup"),("Cucumber","1/2","cup"),("Jicama","1/2","cup"),
        ("Bell Peppers","1/2","cup"),("Chili Peppers","1/2","cup"),("Radishes","1/2","cup"),
        ("Chayote","1/2","cup"),("Sprouts","1/2","cup"),("Green Beans","1/2","cup"),
        ("Asparagus","1/2","cup"),("Leeks","1/2","cup"),("Hearts of Palm","1/2","cup"),
        ("Chard","Unlimited","N/A"),("Cilantro","Unlimited","N/A"),("Kale","Unlimited","N/A"),
        ("Spinach","Unlimited","N/A"),("Lettuce","Unlimited","N/A"),("Arugula","Unlimited","N/A"),
        ("Purslane","Unlimited","N/A"),("Carrot","1/2","cup"),("Beet","1/2","cup"),
    ],
    "Dairy": [
        ("Lactose-Free Milk","1","cup"),("Greek Yogurt","120","ml"),
        ("Cottage Cheese","35","g"),("Goat Cheese","30","g"),("Ricotta Cheese","50","g"),
    ],
}

DEFAULT_TARGETS = {
    "Protein": 10.0, "Cereals": 6.0, "Vegetables": 6.0,
    "Fats": 4.5, "Fruits": 1.5, "Dairy": 1.5,
}

MEAL_SLOTS = ["Breakfast", "Snack 1", "Lunch", "Snack 2", "Dinner", "General"]

# ── Helper functions ──────────────────────────────────────────────────────────
def to_float(val: str) -> float:
    s = str(val).strip()
    if s in ("Unlimited", "nan", "N/A", ""):
        return 0.0
    try:
        return float(sum(Fraction(p) for p in s.split()))
    except (ValueError, ZeroDivisionError):
        return 0.0

@st.cache_data
def build_lookup():
    """Returns {item_name: (category, portion_float, unit)} for every food."""
    lookup = {}
    for cat, items in RAW_DATA.items():
        for name, size, unit in items:
            lookup[name] = (cat, to_float(size), unit)
    return lookup

def calc_portions(item: str, amount: float, lookup: dict):
    if item not in lookup:
        return None, None
    cat, ref, unit = lookup[item]
    if ref <= 0:
        return 0.0, cat
    raw = amount / ref
    return round(raw * 2) / 2, cat   # rounds to nearest 0.5

def pct_color(pct: float, base_color: str) -> str:
    """Return red if over 110%, else the category colour."""
    return "#e63946" if pct > 1.1 else base_color

# ── Session state init ────────────────────────────────────────────────────────
if "logs" not in st.session_state:
    st.session_state.logs = []          # list of dicts
if "targets" not in st.session_state:
    st.session_state.targets = DEFAULT_TARGETS.copy()
if "search" not in st.session_state:
    st.session_state.search = ""

# ── Sidebar: edit targets ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Daily Targets")
    for cat in DEFAULT_TARGETS:
        st.session_state.targets[cat] = st.number_input(
            f"{CAT_ICONS[cat]} {cat}",
            min_value=0.0, max_value=30.0,
            value=float(st.session_state.targets[cat]),
            step=0.5,
            key=f"target_{cat}",
        )
    if st.button("Reset Logs", type="secondary"):
        st.session_state.logs = []
        st.rerun()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 8px 0 4px;'>
  <div style='font-size:32px;'>🥗</div>
  <div style='font-size:22px; font-weight:800; color:#1a1a2e;'>Daily Tracker</div>
  <div style='font-size:13px; color:#888; margin-top:2px;'>Nutrition exchange system</div>
</div>
""", unsafe_allow_html=True)

# ── Compute progress ──────────────────────────────────────────────────────────
lookup = build_lookup()
progress = {cat: 0.0 for cat in st.session_state.targets}
for entry in st.session_state.logs:
    if entry["category"] in progress:
        progress[entry["category"]] += entry["portions"]

# ── Section 1: Daily Progress ─────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Daily Progress</div>', unsafe_allow_html=True)

for cat, consumed in progress.items():
    target = st.session_state.targets[cat]
    pct = (consumed / target) if target > 0 else 0.0
    color = pct_color(pct, CAT_COLORS.get(cat, "#888"))
    bar_pct = min(pct * 100, 100)

    if pct >= 1.0:
        badge_html = '<span class="badge badge-done">Done ✓</span>'
    elif pct > 1.1:
        badge_html = '<span class="badge badge-over">Over</span>'
    else:
        badge_html = '<span class="badge badge-going">In progress</span>'

    remaining = max(0.0, target - consumed)
    remaining_txt = f"{remaining:.1f} portions left" if remaining > 0 else "Target reached!"

    st.markdown(f"""
    <div class="cat-card" style="--accent:{color};">
      <div class="cat-header">
        <span class="cat-name">{CAT_ICONS.get(cat,"")} {cat}</span>
        <span class="cat-count">{consumed:.1f} / {target:.1f}{badge_html}</span>
      </div>
      <div class="prog-track">
        <div class="prog-fill" style="width:{bar_pct:.1f}%; background:{color};"></div>
      </div>
      <div class="cat-remaining">{remaining_txt}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Section 2: Log a Meal ─────────────────────────────────────────────────────
st.markdown('<div class="section-title">➕ Log a Meal</div>', unsafe_allow_html=True)

all_items = sorted(lookup.keys())

with st.container():
    # Search filter
    search_query = st.text_input(
        "Search food", placeholder="Type to filter...",
        label_visibility="collapsed",
        key="food_search"
    )
    filtered = [i for i in all_items if search_query.lower() in i.lower()] if search_query else all_items

    col1, col2 = st.columns([3, 1])
    with col1:
        selected_food = st.selectbox(
            "Food item", options=filtered,
            label_visibility="collapsed",
            key="food_select"
        )
    with col2:
        # Show unit hint
        if selected_food:
            _, _, unit = lookup[selected_food]
            st.markdown(f"<div style='padding-top:10px;font-size:12px;color:#888;text-align:center'>{unit}</div>",
                        unsafe_allow_html=True)

    amount_input = st.number_input(
        "Amount", min_value=0.0, value=0.0, step=0.5,
        label_visibility="collapsed",
        placeholder="Enter amount...",
        key="amount_input"
    )

    slot = st.selectbox("Meal slot", MEAL_SLOTS, label_visibility="visible", key="slot_select")

    log_btn = st.button("Log Meal", type="primary", use_container_width=True)

    if log_btn:
        if not selected_food:
            st.warning("Please pick a food item.")
        elif amount_input <= 0:
            st.warning("Enter an amount greater than zero.")
        else:
            portions, cat = calc_portions(selected_food, amount_input, lookup)
            if portions is None:
                st.error("Food item not found in database.")
            else:
                st.session_state.logs.append({
                    "food": selected_food,
                    "amount": amount_input,
                    "portions": portions,
                    "category": cat,
                    "slot": slot,
                    "timestamp": pd.Timestamp.now(),
                })
                st.success(f"Logged **{portions:.1f}** {cat} portion(s) from {selected_food}.")
                st.rerun()

# ── Section 3: Meal History ───────────────────────────────────────────────────
if st.session_state.logs:
    st.markdown('<div class="section-title">📋 Today\'s Log</div>', unsafe_allow_html=True)
    for entry in reversed(st.session_state.logs):
        color = CAT_COLORS.get(entry["category"], "#888")
        ts = entry["timestamp"].strftime("%H:%M")
        st.markdown(f"""
        <div class="hist-row">
          <div>
            <span class="hist-item">{CAT_ICONS.get(entry['category'],'')} {entry['food']}</span>
            <span class="hist-meta"> &nbsp;{entry['slot']}</span>
          </div>
          <div style='text-align:right'>
            <span style='font-weight:700;color:{color}'>{entry['portions']:.1f} pts</span><br>
            <span class="hist-meta">{ts}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Quick summary table for export
    with st.expander("Summary table"):
        rows = [{"Food": e["food"], "Slot": e["slot"], "Category": e["category"],
                 "Portions": e["portions"], "Time": e["timestamp"].strftime("%H:%M")}
                for e in st.session_state.logs]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        csv = pd.DataFrame(rows).to_csv(index=False).encode("utf-8")
        st.download_button("Export CSV", csv, "nutrition_log.csv", "text/csv",
                           use_container_width=True)
else:
    st.markdown("""
    <div style='text-align:center;color:#aaa;padding:30px 0 10px;font-size:14px;'>
        No meals logged yet. Use the form above to get started!
    </div>
    """, unsafe_allow_html=True)
