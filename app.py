import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    "Jerk": "Podrzut kettlebell z rack po podwójnym ugięciu nóg. Max powtórzeń: 120.\n\nJerk: Driving the kettlebell up from the rack with leg assistance. Max reps: 120.",
    "Half Snatch": "Rwanie kettlebell nad głowę, zrzut do rack. Max powtórzeń: 108.\n\nHalf Snatch: Snatch the kettlebell overhead, lowering to rack. Max reps: 108.",
    "Strict Push Press": "Wyciskanie kettlebell pojedynyczym ugięciem kolan. Max powtórzeń: 120.\n\nStrict Push Press: Pressing the kettlebell with leg drive. Max reps: 120."
}
#Dodanie obrazka
st.image("logo.png", width=200)


st.title("Kalkulator pięcioboju kettlebell \n Kettlebell Pentathlon Score Calculator")

# Dane wejściowe
results = {}
for exercise in MAX_REPS.keys():
    st.subheader(exercise)
    st.write(EXERCISE_DESCRIPTIONS[exercise])
    weight = st.selectbox(f"Wybierz wagę odważnika -Kettlebell weight (kg) - {exercise}", WEIGHTS, key=f"weight_{exercise}")
    #reps = st.number_input(f"Podaj liczbę powtórzeń -Enter reps- {exercise}", min_value=0, max_value=MAX_REPS[exercise], key=f"reps_{exercise}")
    reps = st.slider(f"Podaj liczbę powtórzeń - Enter reps - {exercise}", 0, MAX_REPS[exercise], key=f"reps_{exercise}")
    points = weight * POINTS_PER_KG * reps
    volume = weight * reps
    results[exercise] = {"weight": weight, "reps": reps, "points": points, "volume": volume}
# st.write(f"{exercise}: waga = {res['weight']}, powtórzenia = {res['reps']}, punkty = {res['points']}")
# Obliczenia sumaryczne

total_points = sum(res["points"] for res in results.values())
total_volume = sum(res["volume"] for res in results.values())
total_reps = sum(res["reps"] for res in results.values())

# Wynik końcowy

st.subheader("Podsumowanie wyników - Summary of results")
st.write(f"**Łączna liczba punktów - Total points:** {total_points / 2}")
st.write(f"**Suma objętości (kg) -Total volume:** {total_volume}")
st.write(f"**Łączna liczba powtórzeń - Total reps:** {total_reps}")

# Wizualizacja wyników
st.subheader("Wizualizacja wyników")
fig, ax = plt.subplots(1, 2, figsize=(12, 5))


# Wykres punktów

ax[0].bar(results.keys(), [res["points"] / 2 for res in results.values()], color='blue')
ax[0].set_title("Punkty za poszczególne boje")
ax[0].set_ylabel("Punkty- Points")
ax[0].set_xlabel("Boje")
ax[0].tick_params(axis='x', rotation=45)



# Wykres objętości
ax[1].bar(results.keys(), [res["volume"] for res in results.values()], color='green')
ax[1].set_title("Objętość treningowa (kg × powtórzenia)")
ax[1].set_ylabel("Objętość")
ax[1].set_xlabel("Boje")
ax[1].tick_params(axis='x', rotation=45)

st.pyplot(fig)

fig_hbar, ax_hbar = plt.subplots(figsize=(8, 5))

# Pobranie danych
exercise_names = list(results.keys())
user_reps = [res["reps"] for res in results.values()]
max_reps = [MAX_REPS[exercise] for exercise in exercise_names]

# Wykres słupkowy poziomy
ax_hbar.barh(exercise_names, max_reps, color='lightgray', label="Max reps")
ax_hbar.barh(exercise_names, user_reps, color='blue', label="Twoje reps")

# Opis osi
ax_hbar.set_xlabel("Liczba powtórzeń")
ax_hbar.set_title("Porównanie Twoich powtórzeń z maksymalnymi")
ax_hbar.legend()
ax_hbar.invert_yaxis()  # Odwrócenie kolejności dla lepszej czytelności

st.subheader("Ile brakowało do maksymalnych powtórzeń?")
st.pyplot(fig_hbar)


# Dane do wykresu
categories = list(results.keys())
values = [res["points"] / 2 for res in results.values()]  
values += values[:1]  # Zamknięcie pętli wykresu

angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]  # Zamknięcie pętli wykresu

fig_radar, ax_radar = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax_radar.fill(angles, values, color='blue', alpha=0.3)
ax_radar.plot(angles, values, color='blue', linewidth=2)
ax_radar.set_xticks(angles[:-1])
ax_radar.set_xticklabels(categories)

st.subheader("Rozkład punktów na bojach (Wykres radarowy)")
st.pyplot(fig_radar)

fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
ax_pie.pie(
    [res["points"] / 2 for res in results.values()],
    labels=results.keys(),
    autopct='%1.1f%%',
    colors=['blue', 'green', 'red', 'purple', 'orange'],
    startangle=90
)
ax_pie.set_title("Procentowy udział punktów w bojach")

st.subheader("Procentowy udział punktów w bojach")
st.pyplot(fig_pie)



# Drugi obrazek na dole
st.image("baner.jpg")

df = pd.DataFrame(results).T  
csv = df.to_csv(index=True).encode('utf-8')  
st.download_button("Pobierz wyniki jako CSV", csv, "wyniki.csv", "text/csv")

