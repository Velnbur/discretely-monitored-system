import numpy as np

class Mathmodelodel():
    def __init__(self, g, y, u):
        self.g = g
        self.y = y
        self.u = u

    def A_(self):
        pass

    def system(self, A_matrix, b):
        A_t = np.linalg.pinv(A_matrix) # обернена матриця
        u = np.dot(A_t, b)
        return u

def main():
    # надаємо умову задачі функцію гріна і тд
    T = 20 #кінцевий час
    A, B = 0, 20


    L0 = 3 # кількість початкових спостережень
    x0 = np.linspace(A, B, num=L0)  # рівномірно розподілені точки
    t0 = [0 for i in range(len(xi_0))] #масив нулів

    Lg = 3 # кількість краєвих спостережень
    xg = np.linspace(A, B, num=Lg)
    tg = np.linspace(0, T, num=Lg)


    #

    M0 = 4
    xm0 = np.random.randint(A, B, size=M0)
    tm0 = np.random.randint(0, T, size=M0)

    Mg = 4
    xmg = np.random.randint(A, B, size=Mg)
    tmg = np.random.randint(0, T, size=Mg)

    model = Mathmodel(g, y, u)
    res = model.result


if __name__ == '__main__':
    main()
