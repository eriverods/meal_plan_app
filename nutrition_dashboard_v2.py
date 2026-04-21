"""
Nutrition Exchange Dashboard - Streamlit App
Features: Dark/Light mode, EN/ES/FR language, custom food entries
Run with: streamlit run nutrition_dashboard.py
"""

import streamlit as st
import pandas as pd
from fractions import Fraction

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nutrition Tracker",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Translations ──────────────────────────────────────────────────────────────
TRANSLATIONS = {
    "en": {
        "app_title": "Daily Tracker",
        "app_subtitle": "Nutrition exchange system",
        "sidebar_language": "Language",
        "sidebar_theme": "Theme",
        "sidebar_light": "☀️ Light",
        "sidebar_dark": "🌙 Dark",
        "sidebar_targets": "Daily Targets",
        "sidebar_reset": "Reset Today's Log",
        "section_progress": "📊 Daily Progress",
        "section_log": "➕ Log a Meal",
        "section_custom": "🧪 Add Custom Food",
        "section_history": "📋 Today's Log",
        "search_placeholder": "Search food...",
        "food_label": "Food item",
        "amount_label": "Amount",
        "slot_label": "Meal slot",
        "log_btn": "Log Meal",
        "slots": ["Breakfast", "Snack 1", "Lunch", "Snack 2", "Dinner", "General"],
        "portions_left": "portions left",
        "target_reached": "Target reached!",
        "badge_done": "Done ✓",
        "badge_over": "Over",
        "badge_going": "In progress",
        "warn_pick": "Please pick a food item.",
        "warn_amount": "Enter an amount greater than zero.",
        "err_notfound": "Item not found in database.",
        "success_log": "Logged **{p:.1f}** {cat} portion(s) from {food}.",
        "no_logs": "No meals logged yet. Use the form above to get started!",
        "summary_table": "Summary table",
        "export_csv": "Export CSV",
        "custom_name": "Food name",
        "custom_category": "Category",
        "custom_portion": "Portion size (number)",
        "custom_unit": "Unit (g, ml, cup, pcs...)",
        "custom_add_btn": "Add to Database",
        "custom_success": "{name} added to {cat}!",
        "custom_warn_name": "Please enter a food name.",
        "custom_warn_portion": "Portion size must be greater than zero.",
        "custom_existing": "Custom foods added:",
        "cat_labels": {
            "Protein": "Protein", "Cereals": "Cereals", "Fats": "Fats",
            "Fruits": "Fruits", "Vegetables": "Vegetables", "Dairy": "Dairy"
        },
    },
    "es": {
        "app_title": "Registro Diario",
        "app_subtitle": "Sistema de intercambios nutricionales",
        "sidebar_language": "Idioma",
        "sidebar_theme": "Tema",
        "sidebar_light": "☀️ Claro",
        "sidebar_dark": "🌙 Oscuro",
        "sidebar_targets": "Metas Diarias",
        "sidebar_reset": "Borrar Registro de Hoy",
        "section_progress": "📊 Progreso del Día",
        "section_log": "➕ Registrar Comida",
        "section_custom": "🧪 Agregar Alimento",
        "section_history": "📋 Registro de Hoy",
        "search_placeholder": "Buscar alimento...",
        "food_label": "Alimento",
        "amount_label": "Cantidad",
        "slot_label": "Tiempo de comida",
        "log_btn": "Registrar",
        "slots": ["Desayuno", "Colación 1", "Comida", "Colación 2", "Cena", "General"],
        "portions_left": "porciones restantes",
        "target_reached": "¡Meta alcanzada!",
        "badge_done": "Listo ✓",
        "badge_over": "Excedido",
        "badge_going": "En progreso",
        "warn_pick": "Por favor selecciona un alimento.",
        "warn_amount": "Ingresa una cantidad mayor a cero.",
        "err_notfound": "Alimento no encontrado en la base de datos.",
        "success_log": "Registradas **{p:.1f}** porción(es) de {cat} — {food}.",
        "no_logs": "Sin registros aún. ¡Usa el formulario de arriba para comenzar!",
        "summary_table": "Tabla resumen",
        "export_csv": "Exportar CSV",
        "custom_name": "Nombre del alimento",
        "custom_category": "Categoría",
        "custom_portion": "Tamaño de porción (número)",
        "custom_unit": "Unidad (g, ml, taza, pzas...)",
        "custom_add_btn": "Agregar a la Base de Datos",
        "custom_success": "¡{name} agregado a {cat}!",
        "custom_warn_name": "Por favor ingresa el nombre del alimento.",
        "custom_warn_portion": "El tamaño de porción debe ser mayor a cero.",
        "custom_existing": "Alimentos personalizados agregados:",
        "cat_labels": {
            "Protein": "Proteína", "Cereals": "Cereales", "Fats": "Grasas",
            "Fruits": "Frutas", "Vegetables": "Verduras", "Dairy": "Lácteos"
        },
    },
    "fr": {
        "app_title": "Suivi Quotidien",
        "app_subtitle": "Système d'échanges nutritionnels",
        "sidebar_language": "Langue",
        "sidebar_theme": "Thème",
        "sidebar_light": "☀️ Clair",
        "sidebar_dark": "🌙 Sombre",
        "sidebar_targets": "Objectifs Journaliers",
        "sidebar_reset": "Réinitialiser le Journal",
        "section_progress": "📊 Progrès du Jour",
        "section_log": "➕ Enregistrer un Repas",
        "section_custom": "🧪 Ajouter un Aliment",
        "section_history": "📋 Journal du Jour",
        "search_placeholder": "Rechercher un aliment...",
        "food_label": "Aliment",
        "amount_label": "Quantité",
        "slot_label": "Moment du repas",
        "log_btn": "Enregistrer",
        "slots": ["Petit-déjeuner", "Collation 1", "Déjeuner", "Collation 2", "Dîner", "Général"],
        "portions_left": "portions restantes",
        "target_reached": "Objectif atteint !",
        "badge_done": "Atteint ✓",
        "badge_over": "Dépassé",
        "badge_going": "En cours",
        "warn_pick": "Veuillez choisir un aliment.",
        "warn_amount": "Entrez une quantité supérieure à zéro.",
        "err_notfound": "Aliment introuvable dans la base de données.",
        "success_log": "**{p:.1f}** portion(s) de {cat} enregistrée(s) — {food}.",
        "no_logs": "Aucun repas enregistré. Utilisez le formulaire ci-dessus !",
        "summary_table": "Tableau récapitulatif",
        "export_csv": "Exporter CSV",
        "custom_name": "Nom de l'aliment",
        "custom_category": "Catégorie",
        "custom_portion": "Taille de portion (nombre)",
        "custom_unit": "Unité (g, ml, tasse, pcs...)",
        "custom_add_btn": "Ajouter à la Base de Données",
        "custom_success": "{name} ajouté à {cat} !",
        "custom_warn_name": "Veuillez entrer le nom de l'aliment.",
        "custom_warn_portion": "La taille de portion doit être supérieure à zéro.",
        "custom_existing": "Aliments personnalisés ajoutés :",
        "cat_labels": {
            "Protein": "Protéines", "Cereals": "Céréales", "Fats": "Graisses",
            "Fruits": "Fruits", "Vegetables": "Légumes", "Dairy": "Produits laitiers"
        },
    },
}

LANG_OPTIONS = {"English": "en", "Español": "es", "Français": "fr"}

# ── Colour palette ────────────────────────────────────────────────────────────
CAT_COLORS = {
    "Protein": "#4361ee", "Cereals": "#f4a261", "Fats": "#e76f51",
    "Fruits": "#2a9d8f", "Vegetables": "#57cc99", "Dairy": "#9b5de5",
}
CAT_ICONS = {
    "Protein": "🥩", "Cereals": "🌾", "Fats": "🥑",
    "Fruits": "🍎", "Vegetables": "🥦", "Dairy": "🥛",
}

# ── Base food data ────────────────────────────────────────────────────────────
BASE_DATA = {
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

# ── Helpers ───────────────────────────────────────────────────────────────────
def to_float(val: str) -> float:
    s = str(val).strip()
    if s in ("Unlimited", "nan", "N/A", ""):
        return 0.0
    try:
        return float(sum(Fraction(p) for p in s.split()))
    except (ValueError, ZeroDivisionError):
        return 0.0

def build_lookup(custom_foods: list) -> dict:
    lookup = {}
    for cat, items in BASE_DATA.items():
        for name, size, unit in items:
            lookup[name] = (cat, to_float(size), unit)
    for entry in custom_foods:
        lookup[entry["name"]] = (entry["category"], entry["portion"], entry["unit"])
    return lookup

def calc_portions(item: str, amount: float, lookup: dict):
    if item not in lookup:
        return None, None
    cat, ref, unit = lookup[item]
    if ref <= 0:
        return 0.0, cat
    return round((amount / ref) * 2) / 2, cat

def pct_color(pct: float, base_color: str) -> str:
    return "#e63946" if pct > 1.1 else base_color

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "logs": [], "targets": DEFAULT_TARGETS.copy(),
    "custom_foods": [], "lang": "en", "dark_mode": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    lang_label = st.selectbox(
        "🌐 Language / Idioma / Langue",
        options=list(LANG_OPTIONS.keys()),
        index=list(LANG_OPTIONS.values()).index(st.session_state.lang),
    )
    st.session_state.lang = LANG_OPTIONS[lang_label]
    T = TRANSLATIONS[st.session_state.lang]

    st.divider()

    st.markdown(f"**{T['sidebar_theme']}**")
    col_l, col_d = st.columns(2)
    with col_l:
        if st.button(T["sidebar_light"], use_container_width=True, key="btn_light"):
            st.session_state.dark_mode = False
            st.rerun()
    with col_d:
        if st.button(T["sidebar_dark"], use_container_width=True, key="btn_dark"):
            st.session_state.dark_mode = True
            st.rerun()

    st.divider()

    st.markdown(f"**{T['sidebar_targets']}**")
    for cat in DEFAULT_TARGETS:
        label = T["cat_labels"][cat]
        st.session_state.targets[cat] = st.number_input(
            f"{CAT_ICONS[cat]} {label}",
            min_value=0.0, max_value=30.0,
            value=float(st.session_state.targets[cat]),
            step=0.5, key=f"target_{cat}",
        )

    st.divider()
    if st.button(T["sidebar_reset"], use_container_width=True):
        st.session_state.logs = []
        st.rerun()

T = TRANSLATIONS[st.session_state.lang]

# ── Theme tokens ──────────────────────────────────────────────────────────────
if st.session_state.dark_mode:
    BG          = "#0f0f1a"
    CARD_BG     = "#1c1c2e"
    TEXT_MAIN   = "#e8e8f0"
    TEXT_SUB    = "#a0a0b8"
    TEXT_MUTED  = "#606080"
    PROG_TRACK  = "#2a2a3e"
    HIST_BORDER = "#2a2a3e"
    SHADOW      = "rgba(0,0,0,0.3)"
else:
    BG          = "#f7f8fc"
    CARD_BG     = "#ffffff"
    TEXT_MAIN   = "#1a1a2e"
    TEXT_SUB    = "#444466"
    TEXT_MUTED  = "#888899"
    PROG_TRACK  = "#ebebf0"
    HIST_BORDER = "#f0f0f5"
    SHADOW      = "rgba(0,0,0,0.06)"

st.markdown(f"""
<style>
  .stApp {{ background-color: {BG} !important; }}
  .block-container {{ padding: 1rem 1rem 3rem; max-width: 480px; }}
  #MainMenu, footer, header {{ visibility: hidden; }}

  /* Sidebar */
  section[data-testid="stSidebar"] {{ background-color: {CARD_BG} !important; }}
  section[data-testid="stSidebar"] label,
  section[data-testid="stSidebar"] p,
  section[data-testid="stSidebar"] span {{ color: {TEXT_MAIN} !important; }}

  /* General text override for dark mode */
  .stMarkdown p, .stMarkdown li, .stMarkdown span,
  label, .stSelectbox label, .stNumberInput label,
  .stTextInput label, .stExpander p {{
      color: {TEXT_MAIN} !important;
  }}

  /* Category card */
  .cat-card {{
      background: {CARD_BG};
      border-radius: 16px;
      padding: 14px 16px 10px;
      margin-bottom: 12px;
      box-shadow: 0 2px 12px {SHADOW};
      border-left: 4px solid var(--accent);
  }}
  .cat-header {{
      display: flex; justify-content: space-between;
      align-items: baseline; margin-bottom: 6px;
  }}
  .cat-name      {{ font-weight: 700; font-size: 15px; color: {TEXT_MAIN}; }}
  .cat-count     {{ font-size: 13px; color: {TEXT_SUB}; }}
  .cat-remaining {{ font-size: 11px; color: {TEXT_MUTED}; margin-top: 4px; }}

  .prog-track {{
      background: {PROG_TRACK}; border-radius: 8px;
      height: 10px; overflow: hidden; margin-top: 6px;
  }}
  .prog-fill {{ height: 100%; border-radius: 8px; transition: width 0.4s ease; }}

  .badge {{
      display: inline-block; font-size: 10px; font-weight: 600;
      padding: 2px 8px; border-radius: 20px; margin-left: 6px;
  }}
  .badge-done  {{ background: #d4edda; color: #155724; }}
  .badge-over  {{ background: #f8d7da; color: #721c24; }}
  .badge-going {{ background: #e8f4fd; color: #0c5460; }}

  .section-title {{
      font-size: 18px; font-weight: 800;
      color: {TEXT_MAIN}; margin: 20px 0 12px;
  }}

  .hist-row {{
      display: flex; justify-content: space-between;
      padding: 7px 0; border-bottom: 1px solid {HIST_BORDER};
      font-size: 13px;
  }}
  .hist-item {{ color: {TEXT_MAIN}; font-weight: 500; }}
  .hist-meta {{ color: {TEXT_MUTED}; font-size: 11px; }}
  .empty-state {{ text-align:center; color:{TEXT_MUTED}; padding:30px 0 10px; font-size:14px; }}

  div[data-testid="stSelectbox"] > div  {{ border-radius: 10px !important; }}
  div[data-testid="stNumberInput"] input {{ border-radius: 10px !important; }}
  div[data-testid="stTextInput"] input   {{ border-radius: 10px !important; color: {TEXT_MAIN} !important; }}
  button[kind="primary"] {{ border-radius: 12px !important; font-weight: 700 !important; }}
  div[data-testid="stSuccess"], div[data-testid="stWarning"] {{ border-radius: 12px; }}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='text-align:center; padding: 8px 0 4px;'>
  <div style='font-size:32px;'>🥗</div>
  <div style='font-size:22px; font-weight:800; color:{TEXT_MAIN};'>{T["app_title"]}</div>
  <div style='font-size:13px; color:{TEXT_MUTED}; margin-top:2px;'>{T["app_subtitle"]}</div>
</div>
""", unsafe_allow_html=True)

# ── Build lookup ──────────────────────────────────────────────────────────────
lookup = build_lookup(st.session_state.custom_foods)

# ── Compute progress ──────────────────────────────────────────────────────────
progress = {cat: 0.0 for cat in st.session_state.targets}
for entry in st.session_state.logs:
    if entry["category"] in progress:
        progress[entry["category"]] += entry["portions"]

# ── Section 1: Daily Progress ─────────────────────────────────────────────────
st.markdown(f'<div class="section-title">{T["section_progress"]}</div>', unsafe_allow_html=True)

for cat, consumed in progress.items():
    target  = st.session_state.targets[cat]
    pct     = (consumed / target) if target > 0 else 0.0
    color   = pct_color(pct, CAT_COLORS.get(cat, "#888"))
    bar_pct = min(pct * 100, 100)
    label   = T["cat_labels"][cat]

    if pct >= 1.0:
        badge_html = f'<span class="badge badge-done">{T["badge_done"]}</span>'
    elif pct > 1.1:
        badge_html = f'<span class="badge badge-over">{T["badge_over"]}</span>'
    else:
        badge_html = f'<span class="badge badge-going">{T["badge_going"]}</span>'

    remaining     = max(0.0, target - consumed)
    remaining_txt = f"{remaining:.1f} {T['portions_left']}" if remaining > 0 else T["target_reached"]

    st.markdown(f"""
    <div class="cat-card" style="--accent:{color};">
      <div class="cat-header">
        <span class="cat-name">{CAT_ICONS.get(cat,"")} {label}</span>
        <span class="cat-count">{consumed:.1f} / {target:.1f}{badge_html}</span>
      </div>
      <div class="prog-track">
        <div class="prog-fill" style="width:{bar_pct:.1f}%; background:{color};"></div>
      </div>
      <div class="cat-remaining">{remaining_txt}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Section 2: Log a Meal ─────────────────────────────────────────────────────
st.markdown(f'<div class="section-title">{T["section_log"]}</div>', unsafe_allow_html=True)

all_items    = sorted(lookup.keys())
search_query = st.text_input(
    T["food_label"], placeholder=T["search_placeholder"],
    label_visibility="collapsed", key="food_search"
)
filtered = [i for i in all_items if search_query.lower() in i.lower()] if search_query else all_items

col1, col2 = st.columns([3, 1])
with col1:
    selected_food = st.selectbox(
        T["food_label"], options=filtered,
        label_visibility="collapsed", key="food_select"
    )
with col2:
    if selected_food and selected_food in lookup:
        _, _, unit = lookup[selected_food]
        st.markdown(
            f"<div style='padding-top:10px;font-size:12px;color:{TEXT_MUTED};text-align:center'>{unit}</div>",
            unsafe_allow_html=True
        )

amount_input = st.number_input(
    T["amount_label"], min_value=0.0, value=0.0, step=0.5,
    label_visibility="collapsed", key="amount_input"
)
slot = st.selectbox(T["slot_label"], T["slots"], key="slot_select")

if st.button(T["log_btn"], type="primary", use_container_width=True):
    if not selected_food:
        st.warning(T["warn_pick"])
    elif amount_input <= 0:
        st.warning(T["warn_amount"])
    else:
        portions, cat = calc_portions(selected_food, amount_input, lookup)
        if portions is None:
            st.error(T["err_notfound"])
        else:
            st.session_state.logs.append({
                "food": selected_food, "amount": amount_input,
                "portions": portions, "category": cat,
                "slot": slot, "timestamp": pd.Timestamp.now(),
            })
            st.success(T["success_log"].format(
                p=portions, cat=T["cat_labels"][cat], food=selected_food
            ))
            st.rerun()

# ── Section 3: Add Custom Food ────────────────────────────────────────────────
st.markdown(f'<div class="section-title">{T["section_custom"]}</div>', unsafe_allow_html=True)

with st.expander(T["section_custom"], expanded=False):
    c_name    = st.text_input(T["custom_name"], key="c_name")
    c_cat     = st.selectbox(
        T["custom_category"],
        options=list(DEFAULT_TARGETS.keys()),
        format_func=lambda x: T["cat_labels"][x],
        key="c_cat"
    )
    c_portion = st.number_input(T["custom_portion"], min_value=0.0, step=0.5, key="c_portion")
    c_unit    = st.text_input(T["custom_unit"], value="g", key="c_unit")

    if st.button(T["custom_add_btn"], use_container_width=True, key="custom_add"):
        if not c_name.strip():
            st.warning(T["custom_warn_name"])
        elif c_portion <= 0:
            st.warning(T["custom_warn_portion"])
        else:
            st.session_state.custom_foods.append({
                "name": c_name.strip(),
                "category": c_cat,
                "portion": c_portion,
                "unit": c_unit.strip() or "g",
            })
            st.success(T["custom_success"].format(
                name=c_name.strip(), cat=T["cat_labels"][c_cat]
            ))
            st.rerun()

    if st.session_state.custom_foods:
        st.markdown(f"<div style='color:{TEXT_MUTED};font-size:12px;margin-top:8px;'>{T['custom_existing']}</div>",
                    unsafe_allow_html=True)
        for cf in st.session_state.custom_foods:
            st.markdown(
                f"<div style='font-size:13px;color:{TEXT_SUB};padding:3px 0;'>"
                f"{CAT_ICONS.get(cf['category'],'')} <b>{cf['name']}</b> "
                f"— {cf['portion']} {cf['unit']} ({T['cat_labels'][cf['category']]})</div>",
                unsafe_allow_html=True
            )

# ── Section 4: Meal History ───────────────────────────────────────────────────
if st.session_state.logs:
    st.markdown(f'<div class="section-title">{T["section_history"]}</div>', unsafe_allow_html=True)
    for entry in reversed(st.session_state.logs):
        color     = CAT_COLORS.get(entry["category"], "#888")
        ts        = entry["timestamp"].strftime("%H:%M")
        cat_label = T["cat_labels"].get(entry["category"], entry["category"])
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

    with st.expander(T["summary_table"]):
        rows = [{
            "Food": e["food"], "Slot": e["slot"],
            "Category": T["cat_labels"].get(e["category"], e["category"]),
            "Portions": e["portions"],
            "Time": e["timestamp"].strftime("%H:%M")
        } for e in st.session_state.logs]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        csv = pd.DataFrame(rows).to_csv(index=False).encode("utf-8")
        st.download_button(T["export_csv"], csv, "nutrition_log.csv", "text/csv",
                           use_container_width=True)
else:
    st.markdown(f'<div class="empty-state">{T["no_logs"]}</div>', unsafe_allow_html=True)
