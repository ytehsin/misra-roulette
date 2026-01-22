import streamlit as st
import pandas as pd
import random
from difflib import SequenceMatcher

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="Misra Roulette", page_icon="🎲")
st.title("🎲 Misra Roulette")
st.write("Enter a Roman Urdu misra-e-oola. Mostly wrong. Rarely right. 😈")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    df = pd.read_csv("table.csv").dropna()
    df["oola"] = df["oola"].str.strip()
    df["saani"] = df["saani"].str.strip()
    return df

df = load_data()

# Oola → correct saani mapping
oola_to_saani = dict(zip(df["oola"], df["saani"]))

# All saani pool (for wrong answers)
all_saani = df["saani"].tolist()

# ---------- SIMILARITY FUNCTION ----------
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# ---------- USER INPUT ----------
oola_input = st.text_input("✍️ Misra-e-Oola (Roman Urdu):")

if st.button("🎲 Play"):
    if not oola_input.strip():
        st.warning("Kuch likhiye, Jaani 😄")
    else:
        # Find best fuzzy match
        best_match = None
        best_score = 0

        for key in oola_to_saani:
            score = similarity(oola_input, key)
            if score > best_score:
                best_score = score
                best_match = key

        # 50% threshold
        if best_score < 0.5:
            st.error("Misra samajh nahi aaya… phir likhiye 😅")
        else:
            # Show matched oola quietly
            st.caption(f"Matched ({int(best_score*100)}%): {best_match}")

            chance = random.randint(1, 20)

            if chance == 1:
                st.success("Jaani (ab khoon thookiye!) 🩸")
                st.markdown(f"**{oola_to_saani[best_match]}**")
            else:
                wrong_pool = [
                    s for s in all_saani if s != oola_to_saani[best_match]
                ]
                st.info("Jaani (phir koshish kijie) 😌")
                st.markdown(f"**{random.choice(wrong_pool)}**")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Mostly ghalat. Kabhi kabhi durust. © Misra Roulette")
