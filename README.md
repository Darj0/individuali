# individuali
# Paralelinė matricų daugyba naudojant MPI

## 1. Problema
Užduotis: efektyviai padauginti dvi dideles n×n sveikųjų skaičių matricas A ir B, naudojant mpi4py. Matricų daugyba yra O(N³) uždavinys, tai reiškia, kad ji reikalauja daug skaičiavimo resursų — todėl puikiai tinka parodyti paralelinį greitėjimą.

Sprendimas: rangas 0 sugeneruoja matricas, padalina A eilutėmis tarp rangų, kiekvienas rangas padaugina savo eilutes su visų B matricos eilučių ir gražina rezultato dalį atgal.


## 2. Duomenys

Programa generuoja dvi atsitiktines n x n matricas (panaudota funkcija "np.random.randint(0, 10, size=(n, n))") su ta pačia atsitiktinių skaičių seka (panaudotas "np.random.seed(1234)")

## 3. Algoritmo schema

Kiekvienas procesas gauna savo rangą ir bendrą procesų skaičių.
### Pagrindinis procesas (rank 0):
Nustato n reikšmę.

Naudodamas funkciją generuoti(n) sukuria pradinius duomenis: dvi matricas A ir B.

Padalija matricos A eilutes tarp likusių procesų:

Apskaičiuojamas kiekvienam procesui priskirtas eilučių kiekis.

Naudojami comm.send kvietimai matricai A daliai ir visai matricai B siųsti kiekvienam procesui atskirai.

Surenka rezultatus comm.recv kvietimais ir sujungia juos į galutinę matricą C:

Kiekvienas procesas grąžina savo skaičiavimo dalį ir darbo laiką.

Apskaičiuoja maksimalų darbo laiką.

### Pagalbiniai procesai (rank > 0)
Priima savo dalį matricos A ir visą matricą B.

Atlieka paskirtą skaičiavimą (C_dalis = np.dot(A_dalis, B)).

Išsiunčia rezultatą ir savo darbo laiką atgal pagrindiniam procesui.

### MPI aplinkos uždarymas
Rank 0 išveda rezultatus ir baigia programą.

MPI aplinka uždaroma automatiškai programos pabaigoje.


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
Vartotojas įveda matricos dydį n .
Jei Enter paspaudžiamas be įvesties, naudojamas numatytasis n = 10.


## Rezultatų teisingumas ir scaling analizė

### Rezultatų teisingumas
- Kiekvieno proceso gauta dalis matricų daugybos (`C_dalis`) yra sujungiama pagrindiniame procese (`rank 0`) į galutinę rezultatų matricą `C`.  
- Rezultatai patikrinami lyginant su tiesioginiu skaičiavimu viename procese (`np.dot(A, B)`).  
- Jei visos dalys sutampa su vieno proceso rezultatu, laikoma, kad skaičiavimas teisingas.

### Scaling analizė
- Skaičiavimo laikas priklauso nuo procesų skaičiaus (`X`).  
- Lentelėje ar grafike pateikiami šie duomenys:

| Procesų skaičius (X) | Bendras laikas (TX, s) | Speedup (SX) | Efficiency (EX) |
|---------------------|------------------------|--------------|----------------|
| 1                   | TX0                     | 1.0          | 1.0            |
| 2                   | TX2                     | TX0/TX2      | SX/2           |
| 4                   | TX4                     | TX0/TX4      | SX/4           |
| 8                   | TX8                     | TX0/TX8      | SX/8           |

- **TX** – bendras programos skaičiavimo laikas su X procesų  
- **SX** – greičio prieaugis (speedup), apskaičiuojamas kaip `TX0 / TXX`  
- **EX** – efektyvumas (efficiency), apskaičiuojamas kaip `SX / X`  


