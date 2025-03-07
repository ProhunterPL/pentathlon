import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Tabela przeliczeniowa punktów
POINTS_PER_KG = 0.25
WEIGHTS = list(range(8, 66, 2))

# Maksymalne powtórzenia dla bojów
MAX_REPS = {
    "Clean": 120,
    "Long Cycle Press": 60,
    "Jerk": 120,
    "Half Snatch": 108,
    "Strict Push Press": 120
}

# Opisy bojów
EXERCISE_DESCRIPTIONS = {
    "Clean": "Podrzut kettlebell do rack position. Max powtórzeń: 120.\n\nClean: Lifting the kettlebell to the rack position. Max reps: 120.",
    "Long Cycle Press": "Podrzut do rack, następnie wyciskanie. Max powtórzeń: 60.\n\nLong Cycle Press: Lifting to rack, then pressing. Max reps: 60.",
    "Jerk": "WPodrzut kettlebell z rack po podwójnym ugięciu nóg. Max powtórzeń: 120.\n\nJerk: Driving the kettlebell up from the rack with leg assistance. Max reps: 120.",
    "Half Snatch": "Rwanie kettlebell nad głowę, zrzut do rack. Max powtórzeń: 108.\n\nHalf Snatch: Snatch the kettlebell overhead, lowering to rack. Max reps: 108.",
    "Strict Push Press": "Wyciskanie kettlebell pojedynyczym ugięciem kolan. Max powtórzeń: 120.\n\nStrict Push Press: Pressing the kettlebell with leg drive. Max reps: 120."
}
#Dodanie obrazka
st.markdown("""
    <a href="https://incoresports.eu" target="_blank">
        <img src="logo.png" alt="Incore Sports" style="width:100%;">
    </a>
""", unsafe_allow_html=True)

st.title("Kalkulator pięcioboju kettlebell \n Kettlebell Pentathlon Score Calculator")

# Dane wejściowe
results = {}
for exercise in MAX_REPS.keys():
    st.subheader(exercise)
    st.write(EXERCISE_DESCRIPTIONS[exercise])
    weight = st.selectbox(f"Wybierz wagę odważnika -Kettlebell weight (kg) - {exercise}", WEIGHTS, key=f"weight_{exercise}")
    reps = st.number_input(f"Podaj liczbę powtórzeń -Enter reps- {exercise}", min_value=0, max_value=MAX_REPS[exercise], key=f"reps_{exercise}")
    points = weight * POINTS_PER_KG * reps
    volume = weight * reps
    results[exercise] = {"weight": weight, "reps": reps, "points": points, "volume": volume}

# Obliczenia sumaryczne
total_points = sum(res["points"] for res in results.values())
total_volume = sum(res["volume"] for res in results.values())
total_reps = sum(res["reps"] for res in results.values())

# Wynik końcowy
st.subheader("Podsumowanie wyników - Summary of results")
st.write(f"**Łączna liczba punktów -Total points:** {total_points:.2f}")
st.write(f"**Suma objętości (kg) -Total volume:** {total_volume}")
st.write(f"**Łączna liczba powtórzeń - Total reps:** {total_reps}")

# Wizualizacja wyników
st.subheader("Wizualizacja wyników")
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Wykres punktów
ax[0].bar(results.keys(), [res["points"] for res in results.values()], color='blue')
ax[0].set_title("Punkty za poszczególne boje")
ax[0].set_ylabel("Punkty")
ax[0].set_xlabel("Boje")
ax[0].tick_params(axis='x', rotation=45)

# Wykres objętości
ax[1].bar(results.keys(), [res["volume"] for res in results.values()], color='green')
ax[1].set_title("Objętość treningowa (kg × powtórzenia)")
ax[1].set_ylabel("Objętość")
ax[1].set_xlabel("Boje")
ax[1].tick_params(axis='x', rotation=45)

st.pyplot(fig)

# Drugi obrazek na dole
st.markdown("""
    <a href="https://incoresports.eu" target="_blank">
        <img src="baner.jpg" alt="Incore Sports" style="width:100%;">
    </a>
""", unsafe_allow_html=True)

