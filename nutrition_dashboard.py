import streamlit as st
import sqlite3
import pandas as pd
from fractions import Fraction
from streamlit_oauth import OAuth2Component
import base64
import json

# ==========================================
# 1. THE COMPLETE MULTI-LANGUAGE DATASET
# ==========================================
# Format: ("Name", "Size", "Unit")
DATA_EN = {
    "Protein": [("Beef Steak","30","g"), ("Flank Steak","30","g"), ("Chicken Breast","35","g"), ("Salmon","35","g"), ("Panela Cheese","40","g"), ("Beans","1/2","cup"), ("Protein Powder","17","g")],
    "Cereals": [("Cooked Rice","1/3","cup"), ("Cooked Pasta","1/2","cup"), ("Oat Flakes","1/2","cup"), ("Corn Tortilla","1","pc"), ("Salmas","2","pcs")],
    "Fats": [("Avocado","1/3","pc"), ("Olive Oil","1","tbsp"), ("Almonds","10","pcs"), ("Peanut Butter","1.5","tbsp")],
    "Fruits": [("Apple","1","pc"), ("Banana","1/2","pc"), ("Strawberries","1","cup"), ("Mango","1/2","pc"), ("Orange","2","pcs")],
    "Vegetables": [("Broccoli","1/2","cup"), ("Spinach","Unlimited","N/A"), ("Tomato","1/2","cup"), ("Carrot","1/2","cup")],
    "Dairy": [("Lactose-Free Milk","1","cup"), ("Greek Yogurt","120","ml"), ("Cottage Cheese","35","g")]
}

DATA_ES = {
    "Protein": [("Bistec de Res","30","g"), ("Arrachera","30","g"), ("Pechuga de Pollo","35","g"), ("Salmón","35","g"), ("Queso Panela","40","g"), ("Frijoles","1/2","taza"), ("Proteína en Polvo","17","g")],
    "Cereals": [("Arroz Cocido","1/3","taza"), ("Pasta Cocida","1/2","taza"), ("Avena","1/2","taza"), ("Tortilla de Maíz","1","pza"), ("Salmas","2","pzas")],
    "Fats": [("Aguacate","1/3","pza"), ("Aceite de Oliva","1","cda"), ("Almendras","10","pzas"), ("Crema de Cacahuate","1.5","cda")],
    "Fruits": [("Manzana","1","pza"), ("Plátano","1/2","pza"), ("Fresas","1","taza"), ("Mango","1/2","pza"), ("Naranja","2","pzas")],
    "Vegetables": [("Brócoli","1/2","taza"), ("Espinaca","Unlimited","N/A"), ("Jitomate","1/2","taza"), ("Zanahoria","1/2","taza")],
    "Dairy": [("Leche Deslactosada","1","taza"), ("Yogur Griego","120","ml"), ("Queso Cottage","35","g")]
}

DATA_FR = {
    "Protein": [("Steak de Bœuf","30","g"), ("Bavette","30","g"), ("Blanc de Poulet","35","g"), ("Saumon","35","g"), ("Fromage Panela","40","g"), ("Haricots","1/2","tasse"), ("Poudre de Protéine","17","g")],
    "Cereals": [("Riz Cuit","1/3","tasse"), ("Pâtes Cuites","1/2","tasse"), ("Flocons d'Avoine","1/2","tasse"), ("Tortilla de Maïs","1","pc"), ("Salmas","2","pcs")],
    "Fats": [("Avocat","1/3","pc"), ("Huile d'Olive","1","c à s"), ("Amandes","10","pcs"), ("Beurre de Cacahuète","1.5","c à s")],
    "Fruits": [("Pomme","1","pc"), ("Banane","1/2","pc"), ("Fraises","1","tasse"), ("Mangue","1/2","pc"), ("Orange","2","pcs")],
    "Vegetables": [("Brocoli","1/2","tasse"), ("Épinards","Unlimited","N/A"), ("Tomate","1/2","tasse"), ("Carotte","1/2","tasse")],
    "Dairy": [("Lait Sans Lactose","1","tasse"), ("Yaourt Grec","120","ml"), ("Fromage Cottage","35","g")]
}

# ==========================================
# 2. DATABASE MANAGER
# ==========================================
class DatabaseManager:
    def __init__(self, db_name="nutrition.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()
        self.seed_foods_if_empty()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                name TEXT,
                targets TEXT
            )
        ''')
        # Includes unit columns for each language
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS foods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                name_en TEXT,
                name_es TEXT,
                name_fr TEXT,
                portion_size TEXT,
                unit_en TEXT,
                unit_es TEXT,
                unit_fr TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meal_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                date TEXT,
                slot TEXT,
                category TEXT,
                food_id INTEGER,
                portions REAL,
                FOREIGN KEY(email) REFERENCES users(email),
                FOREIGN KEY(food_id) REFERENCES foods(id)
            )
        ''')
        self.conn.commit()

    def seed_foods_if_empty(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM foods")
        if cursor.fetchone()[0] == 0:
            for cat in DATA_EN.keys():
                for en, es, fr in zip(DATA_EN[cat], DATA_ES[cat], DATA_FR[cat]):
                    cursor.execute('''
                        INSERT INTO foods (
                            category, name_en, name_es, name_fr, 
                            portion_size, unit_en, unit_es, unit_fr
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (cat, en[0], es[0], fr[0], en[1], en[2], es[2], fr[2]))
            self.conn.commit()

    def get_or_create_user(self, email, name, default_targets):
        cursor = self.conn.cursor()
        cursor.execute("SELECT targets FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        if result:
            return eval(result[0])
        else:
            cursor.execute("INSERT INTO users (email, name, targets) VALUES (?, ?, ?)", 
                           (email, name, str(default_targets)))
            self.conn.commit()
            return default_targets

    def get_foods_by_language(self, lang_code):
        query = f'''
            SELECT id, category, 
                   name_{lang_code} as name, 
                   portion_size, 
                   unit_{lang_code} as unit 
            FROM foods
        '''
        return pd.read_sql_query(query, self.conn)

    def log_meal(self, email, food_id, category, portions, slot):
        cursor = self.conn.cursor()
        today = pd.Timestamp.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO meal_logs (email, date, slot, category, food_id, portions)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, today, slot, category, food_id, portions))
        self.conn.commit()

    def get_user_logs_today(self, email, lang_code):
        today = pd.Timestamp.now().strftime('%Y-%m-%d')
        query = f'''
            SELECT m.log_id, m.slot, m.category, m.portions, 
                   f.name_{lang_code} as food_name, f.portion_size, f.unit_{lang_code} as unit
            FROM meal_logs m
            JOIN foods f ON m.food_id = f.id
            WHERE m.email = ? AND m.date = ?
        '''
        return pd.read_sql_query(query, self.conn, params=(email, today)).to_dict('records')

# ==========================================
# 3. HELPER FUNCTIONS & UI STRINGS
# ==========================================
def to_float(val: str) -> float:
    s = str(val).strip()
    if s in ("Unlimited", "nan", "N/A", ""): return 0.0
    try: return float(sum(Fraction(p) for p in s.split()))
    except: return 0.0

TRANSLATIONS = {
    "en": {"title": "Daily Tracker", "log_btn": "Log Meal", "food": "Food item", "cat": "Category"},
    "es": {"title": "Registro Diario", "log_btn": "Registrar", "food": "Alimento", "cat": "Categoría"},
    "fr": {"title": "Suivi Quotidien", "log_btn": "Enregistrer", "food": "Aliment", "cat": "Catégorie"}
}

# ==========================================
# 4. STREAMLIT APP & AUTHENTICATION
# ==========================================
st.set_page_config(page_title="Nutrition Tracker", page_icon="🥗", layout="centered")

if 'db' not in st.session_state:
    st.session_state.db = DatabaseManager()

# Setup Google OAuth
try:
    CLIENT_ID = st.secrets["google"]["client_id"]
    CLIENT_SECRET = st.secrets["google"]["client_secret"]
    REDIRECT_URI = st.secrets["google"]["redirect_uri"]
except FileNotFoundError:
    st.error("Missing `.streamlit/secrets.toml`. Please create it with your Google credentials.")
    st.stop()

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_TOKEN_URL = "https://oauth2.googleapis.com/revoke"

oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, TOKEN_URL, REVOKE_TOKEN_URL)

# Login Screen
if 'user_email' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🥗 Nutrition Tracker</h1>", unsafe_allow_html=True)
    
    result = oauth2.authorize_button(
        name="Continue with Google",
        icon="https://www.google.com/favicon.ico",
        redirect_uri=REDIRECT_URI,
        scope="email profile",
        key="google_login",
        use_container_width=True
    )
    
    if result:
        id_token = result["token"]["id_token"]
        payload = id_token.split(".")[1]
        payload += "=" * ((4 - len(payload) % 4) % 4)
        user_info = json.loads(base64.b64decode(payload).decode("utf-8"))
        
        email = user_info["email"]
        name = user_info.get("name", "User")
        
        default_targets = {"Protein": 10.0, "Cereals": 6.0, "Vegetables": 6.0, "Fats": 4.5, "Fruits": 1.5, "Dairy": 1.5}
        st.session_state.targets = st.session_state.db.get_or_create_user(email, name, default_targets)
        st.session_state.user_email = email
        st.session_state.user_name = name
        st.rerun()
    st.stop()

# ==========================================
# 5. MAIN DASHBOARD (LOGGED IN)
# ==========================================
if 'lang' not in st.session_state: st.session_state.lang = "en"
if 'dark_mode' not in st.session_state: st.session_state.dark_mode = False

with st.sidebar:
    st.markdown(f"**👤 {st.session_state.user_name}**")
    if st.button("Logout", use_container_width=True):
        del st.session_state.user_email
        st.rerun()
    st.divider()
    
    lang_map = {"English": "en", "Español": "es", "Français": "fr"}
    lang_label = st.selectbox("🌐 Language", options=list(lang_map.keys()), index=list(lang_map.values()).index(st.session_state.lang))
    st.session_state.lang = lang_map[lang_label]
    st.session_state.dark_mode = st.toggle("🌙 / ☀️ Modo", value=st.session_state.dark_mode)

T = TRANSLATIONS[st.session_state.lang]

# Fetch user logs and food list for the selected language
logs = st.session_state.db.get_user_logs_today(st.session_state.user_email, st.session_state.lang)
food_df = st.session_state.db.get_foods_by_language(st.session_state.lang)

st.title(f"🥗 {T['title']}")

# Progress Section
progress = {cat: 0.0 for cat in st.session_state.targets}
for log in logs:
    if log["category"] in progress:
        progress[log["category"]] += log["portions"]

for cat, target in st.session_state.targets.items():
    consumed = progress[cat]
    st.write(f"**{cat}**: {consumed:.1f} / {target:.1f}")
    st.progress(min(consumed/target, 1.0) if target > 0 else 0)
st.divider()

# Log Meal Form
st.subheader(T["log_btn"])
categories = food_df['category'].unique().tolist()
selected_cat = st.selectbox(T["cat"], ["All"] + categories)

filtered_df = food_df if selected_cat == "All" else food_df[food_df['category'] == selected_cat]

col1, col2 = st.columns(2)
with col1:
    # Build a lookup dictionary for the dropdown: display name -> corresponding row data
    food_options = {row['name']: row for _, row in filtered_df.iterrows()}
    selected_name = st
