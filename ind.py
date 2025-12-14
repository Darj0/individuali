from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rangas = comm.Get_rank()
procesu_sk = comm.Get_size()

def generuoti(n):
    np.random.seed(1234)
    A = np.random.randint(0, 10, size=(n, n))
    B = np.random.randint(0, 10, size=(n, n))
    return A, B

def main():
    if rangas == 0:
        n = 1000
    else:
        n = None

    n = comm.bcast(n, root=0)


    if rangas == 0:
        A, B = generuoti(n)
    else:
        A = None
        B = np.empty((n, n), dtype=int)

    comm.Bcast(B, root=0)

    blokai = np.array_split(A, procesu_sk, axis=0) if rangas == 0 else None
    A_dalis = comm.scatter(blokai, root=0)

    t_pradzia = MPI.Wtime()
    C_dalis = np.dot(A_dalis, B)
    t_pabaiga = MPI.Wtime()
    darbo_laikas = t_pabaiga - t_pradzia

    max_laikas = comm.reduce(darbo_laikas, op=MPI.MAX, root=0)


    C = comm.gather(C_dalis, root=0)
    eiluciu_sk = comm.gather(A_dalis.shape[0], root=0)

    if rangas == 0:
        C = np.vstack(C)
        print(f"\n=== Maksimalus darbo laikas: {max_laikas:.6f} sek ===")
        print(f"C matricos pradzia:\n{C[:5, :5]}")
        print(f"C matricos pabaiga:\n{C[-5:, -5:]}")
        print(f"Procesu skaicius: {procesu_sk}\n")
        for p, e in enumerate(eiluciu_sk):
            print(f"Procesas {p} gavo {e} eiluciu")

if __name__ == "__main__":
    main()
