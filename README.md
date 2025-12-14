
# Paralelinė matricų daugyba naudojant MPI

## 1. Problema
Užduotis: efektyviai padauginti dvi dideles n×n sveikųjų skaičių matricas A ir B, naudojant mpi4py. Matricų daugyba yra O(N³) uždavinys, tai reiškia, kad ji reikalauja daug skaičiavimo resursų — todėl puikiai tinka paraleliniam apdorojimui.

Sprendimas: pagrindinis procesas sugeneruoja matricas, padalija A eilutėmis tarp procesų. Kiekvienas procesas padaugina savo eilutes su visa B matrica ir grąžina rezultatą pagrindiniam procesui.


## 2. Duomenys

Programa generuoja dvi atsitiktines n x n matricas (panaudota funkcija "np.random.randint(0, 10, size=(n, n))". Kiekvienas matricų elementas yra sveikasis skaičius nuo 0 iki 9. Siekiant užtikrinti rezultatų atkartojamumą, prieš generuojant duomenis nustatoma ta pati atsitiktinių skaičių seka, naudojant "np.random.seed(1234)"

## 3. Algoritmo schema

### Pagrindinis procesas (rank 0):
- Nustato matricos dydį n = 1000;
- Išsiunčia matricos dydį n visiems procesams naudodamas
comm.bcast(n, root=0);

- Naudodamas funkciją generuoti(n) sukuria pradinius duomenis: dvi matricas A ir B.
- Išsiunčia visą matricą B visiems procesams naudodamas
"comm.Bcast(B, root=0)";
- Padalina matricą A į eilučių blokus pagal procesų skaičių, naudodamas
"np.array_split(A, procesu_sk, axis=0)";
- Išskirsto matricos A dalis visiems procesams naudodamas
"comm.scatter(blokai, root=0)";
- Surenka iš visų procesų apskaičiuotas dalines rezultato matricos C dalis naudodamas
"comm.gather(C_dalis, root=0)";
- Gauna maksimalų darbo laiką su funkcija "comm.reduce(darbo_laikas, op=MPI.MAX, root=0)";
- Sujungia gautas C dalis į vieną matricą naudodamas "np.vstack(C)";
- Išveda: maksimalų darbo laiką, rezultato matricos C pradžią, rezultato matricos C pabaigą, procesų skaičių, kiek eilučių gavo kiekvienas procesas.

### Pagalbiniai procesai (rank > 0)
- Priima savo dalį matricos A ir visą matricą B;

- Atlieka paskirtą skaičiavimą (C_dalis = np.dot(A_dalis, B));

- Išsiunčia rezultatą ir savo darbo laiką atgal pagrindiniam procesui.


## 4. Paleidimo instrukcijos

Reikalavimai:
- Python 3.x
- Bibliotekos: mpi4py, numpy
Įdiegimas:
Įdiekite mpi4py (jei dar neįdiegta):
- pip install mpi4py numpy

  
Paleidimas:

Paleidimas rankiniu būdu:

Paleidimas su X procesais (pvz., 4 procesai):
- mpirun -n 4 python ind.py
  
Paleidimas naudojant reprodukcijos skriptą (paleidžia programą su 1, 2, 4, 6, 8 procesais):

Įsitikinkite, kad skriptas turi vykdymo teises:

- chmod +x run.sh
  
Pateiktą paleidimo skriptą run.sh galima paleisti taip:

- ./run.sh

## 5. Rezultatų teisingumas ir scaling analizė

### Rezultatų teisingumas
- Kiekvieno proceso gauta dalis matricų daugybos yra sujungiama pagrindiniame procese į galutinę rezultatų matricą C.   
- Skaičiavimai laikomi teisingais, nes naudojant skirtingą procesų skaičių rezultatas gaunamas identiškas (programa išveda matricos pradžios ir pabaigos submatricas 5x5).

### Scaling analizė


| Procesų skaičius (X) | Maksimalus laikas (s) |       Sₓ          |           Eₓ          |
|---------------------|----------------------|---------------------|-----------------------|
| 1                   | 0.934892             | 1.00                | 1.00                  |
| 2                   | 0.532344             | 1.76                | 0.88                  |
| 4                   | 0.277094             | 3.37                | 0.84                  |
| 6                   | 0.244560             | 3.82                | 0.64                  |
| 8                   | 0.200840             | 4.65                | 0.58                  |

- **Tₓ** – bendras programos skaičiavimo laikas su X procesų  
- **Sₓ** – greičio prieaugis (Tₓ₀ / Tₓₓ)
- **Eₓ** – efektyvumas (Sₓ  / X)


