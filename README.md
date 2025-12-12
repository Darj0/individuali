
# Paralelinė matricų daugyba naudojant MPI

## 1. Problema
Užduotis: efektyviai padauginti dvi dideles n×n sveikųjų skaičių matricas A ir B, naudojant mpi4py. Matricų daugyba yra O(N³) uždavinys, tai reiškia, kad ji reikalauja daug skaičiavimo resursų — todėl puikiai tinka paraleliniam apdorojimui.

Sprendimas: pagrindinis procesas (rank 0) sugeneruoja matricas, padalija A eilutėmis tarp procesų. Kiekvienas procesas padaugina savo eilutes su visa B matrica ir grąžina rezultatą pagrindiniam procesui.


## 2. Duomenys

Programa generuoja dvi atsitiktines n x n matricas (panaudota funkcija "np.random.randint(0, 10, size=(n, n))") su ta pačia atsitiktinių skaičių seka (panaudotas "np.random.seed(1234)")

## 3. Algoritmo schema

Kiekvienas procesas gauna savo rangą ir bendrą procesų skaičių.
### Pagrindinis procesas (rank 0):
Nustato matricos dydį n = 1000.

Naudodamas funkciją generuoti(n) sukuria pradinius duomenis: dvi matricas A ir B.

Išskirsto A matricos eilutes tarp procesų naudodamas "comm.scatter";

Siunčia visiems procesams visą B matricą naudojant "comm.Bcast";

Surenka visų procesų rezultatus (C_dalis) naudodamas "comm.gather" ir sujungia į galutinę matricą C;

Surenka darbo laikus iš visų procesų ir apskaičiuoja maksimalų darbo laiką.

### Pagalbiniai procesai (rank > 0)
Priima savo dalį matricos A ir visą matricą B.

Atlieka paskirtą skaičiavimą (C_dalis = np.dot(A_dalis, B)).

Išsiunčia rezultatą ir savo darbo laiką atgal pagrindiniam procesui.


## 4. Paleidimo instrukcijos

Reikalavimai:
- Python 3.x
- Bibliotekos: mpi4py, numpy
Įdiegimas:
Įdiekite mpi4py (jei dar neįdiegta):
- pip install mpi4py numpy
Įsitikinkite, kad turite MPI įrankį:
- mpirun --version
Paleidimas:
Paleidimas su X procesais (pvz., 4 procesai):
mpirun -n 4 python individuali.py


## Rezultatų teisingumas ir scaling analizė

### Rezultatų teisingumas
- Kiekvieno proceso gauta dalis matricų daugybos (`C_dalis`) yra sujungiama pagrindiniame procese (`rank 0`) į galutinę rezultatų matricą `C`.   
- Skaičiavimai laikomi teisingais, nes naudojant skirtingą procesų skaičių rezultatas gaunamas identiškas.

### Scaling analizė
- Skaičiavimo laikas priklauso nuo procesų skaičiaus (`X`).  
- Lentelėje ar grafike pateikiami šie duomenys:

| Procesų skaičius (X) | Bendras laikas (TX, s) | Speedup (SX) | Efficiency (EX) |
|---------------------|------------------------|--------------|----------------|
| 2                   | 0,544                     | 1,0          | 1.0            |
| 4                   | 0,4                       | 1,36      | SX/2           |
| 6                   | 0,297                     | 1,83      | SX/4           |
| 8                   | 0,227                     | 2,4      | SX/8           |

- **TX** – bendras programos skaičiavimo laikas su X procesų  
- **SX** – greičio prieaugis (speedup), apskaičiuojamas kaip `TX0 / TXX`  
- **EX** – efektyvumas (efficiency), apskaičiuojamas kaip `SX / X`  


