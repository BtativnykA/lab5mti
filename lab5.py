import math

# ГЛОБАЛЬНИЙ ЛІЧИЛЬНИК ОБЧИСЛЕНЬ ФУНКЦІЇ
_call_count = 0

# ПІДІНТЕГРАЛЬНА ФУНКЦІЯ
def f(x):
    """f(x) = 50 + 20·sin(πx/12) + 5·e^(-0.2(x-12)²)."""
    global _call_count
    _call_count += 1
    return 50 + 20 * math.sin(math.pi * x / 12) + 5 * math.exp(-0.2 * (x - 12) ** 2)

# АНАЛІТИЧНА ПЕРВІСНА
def F_analytic(x):
    """
    F(x) = 50x - (240/π)·cos(πx/12) + (5/2)·√(5π)·erf(√0.2·(x-12)).
    """
    term1 = 50 * x
    term2 = -(240 / math.pi) * math.cos(math.pi * x / 12)
    term3 = (5 / 2) * math.sqrt(5 * math.pi) * math.erf(math.sqrt(0.2) * (x - 12))
    return term1 + term2 + term3


# СКЛАДОВА ФОРМУЛА СІМПСОНА
def simpson(a, b, N):
    """I(N) = h/3 · (f₀ + 4Σf_непарн + 2Σf_парн + f_N)."""
    if N % 2 != 0:
        N += 1
    h = (b - a) / N
    s = f(a) + f(b)
    for i in range(1, N):
        x = a + i * h
        s += (4 if i % 2 else 2) * f(x)
    return h / 3 * s

# АДАПТИВНИЙ АЛГОРИТМ (рекурсивний Сімпсон)
def adaptive_simpson(a, b, eps, whole=None, depth=0, max_depth=30):
    c = (a + b) / 2
    if whole is None:
        whole = (b - a) / 6 * (f(a) + 4 * f(c) + f(b))
    left = (c - a) / 6 * (f(a) + 4 * f((a + c) / 2) + f(c))
    right = (b - c) / 6 * (f(c) + 4 * f((c + b) / 2) + f(b))
    refined = left + right

    if depth >= max_depth or abs(refined - whole) < 15 * eps:
        return refined, depth

    r1, d1 = adaptive_simpson(a, c, eps / 2, left, depth + 1, max_depth)
    r2, d2 = adaptive_simpson(c, b, eps / 2, right, depth + 1, max_depth)
    return r1 + r2, max(d1, d2)

# ГОЛОВНА ПРОГРАМА
def main():
    global _call_count

    a, b = 0.0, 24.0
    I_exact = F_analytic(b) - F_analytic(a)

    print("=" * 70)
    print("ЛАБОРАТОРНА РОБОТА №5")
    print("Чисельне інтегрування. Сімпсон. Рунге-Ромберг. Ейткен. Адаптивний")
    print("=" * 70)

    print("\nПУНКТ 1-2: Аналітичне значення інтегралу")
    print("-" * 50)
    print("f(x) = 50 + 20·sin(πx/12) + 5·e^(-0.2(x-12)²)")
    print(f"[a, b] = [{a}, {b}]")
    print(f"I₀ = {I_exact:.12f}")

    print("\n" + "=" * 70)
    print("ПУНКТ 3-4: Залежність похибки від N (Сімпсон)")
    print("=" * 70)

    Ns = list(range(10, 1001, 2))
    epsilons = []
    for N in Ns:
        I_N = simpson(a, b, N)
        epsilons.append(abs(I_N - I_exact))

    eps_target = 1e-12
    N_opt, eps_opt = None, None
    for N, eps in zip(Ns, epsilons):
        if eps < eps_target:
            N_opt, eps_opt = N, eps
            break

    if N_opt is None:
        idx = epsilons.index(min(epsilons))
        N_opt, eps_opt = Ns[idx], epsilons[idx]
        print(f"\nПри N ≤ 1000 ε = 1e-12 не досягається.")
        print(f"Беремо N_opt = {N_opt}, ε_opt = {eps_opt:.6e}")
    else:
        print(f"\nN_opt = {N_opt}, ε_opt = {eps_opt:.6e}")

    print(f"Перевірка: I({N_opt}) = {simpson(a, b, N_opt):.12f}")

    print("\n" + "=" * 70)
    print("ПУНКТ 5: Обчислення при N₀ (кратне 8)")
    print("=" * 70)

    N0 = 24
    print(f"N_opt = {N_opt}")
    print(f"N₀ = {N0} (кратне 8, ділиться на 2 і 4)")
    print(f"N₀ кратне 8: {N0 % 8 == 0}, кратне 4: {N0 % 4 == 0}, кратне 2: {N0 % 2 == 0}")

    I_N0 = simpson(a, b, N0)
    eps_0 = abs(I_N0 - I_exact)
    print(f"\nI(N₀) = {I_N0:.12f}")
    print(f"ε₀ = |I(N₀) - I₀| = {eps_0:.6e}")

    print("\n" + "=" * 70)
    print("ПУНКТ 6: Метод Рунге-Ромберга")
    print("=" * 70)

    I_N0_half = simpson(a, b, N0 // 2)
    # p = 4 для Сімпсона, q = 2 → q^p - 1 = 15
    I_RR = I_N0 + (I_N0 - I_N0_half) / (2 ** 4 - 1)
    eps_RR = abs(I_RR - I_exact)

    print(f"I(N₀)   = I({N0})   = {I_N0:.12f}")
    print(f"I(N₀/2) = I({N0//2})  = {I_N0_half:.12f}")
    print(f"\nФормула: I_RR = I(N₀) + (I(N₀) - I(N₀/2)) / (2^p - 1)")
    print(f"p = 4 (Сімпсон), q = 2 → q^p - 1 = 15")
    print(f"\nI_RR = {I_RR:.12f}")
    print(f"ε_RR = |I_RR - I₀| = {eps_RR:.6e}")

    print("\n" + "=" * 70)
    print("ПУНКТ 7: Метод Ейткена")
    print("=" * 70)

    I_N0_quarter = simpson(a, b, N0 // 4)
    print(f"I(N₀)   = I({N0})   = {I_N0:.12f}")
    print(f"I(N₀/2) = I({N0//2})  = {I_N0_half:.12f}")
    print(f"I(N₀/4) = I({N0//4})  = {I_N0_quarter:.12f}")

    I_E = (I_N0_half ** 2 - I_N0 * I_N0_quarter) / (2 * I_N0_half - (I_N0 + I_N0_quarter))
    eps_E = abs(I_E - I_exact)

    p_A = math.log(abs((I_N0_quarter - I_N0_half) / (I_N0_half - I_N0))) / math.log(2)

    print(f"\nФормула: I_E = [(I(N₀/2))² - I(N₀)·I(N₀/4)] / [2I(N₀/2) - (I(N₀) + I(N₀/4))]")
    print(f"I_E = {I_E:.12f}")
    print(f"ε_E = |I_E - I₀| = {eps_E:.6e}")
    print(f"\nПорядок точності: p = ln|(I₃-I₂)/(I₂-I₁)|/ln(2)")
    print(f"p = {p_A:.6f}")

    print("\n" + "=" * 70)
    print("ПУНКТ 9: Адаптивний алгоритм")
    print("=" * 70)

    print(f"\n{'δ':>10} | {'I_adapt':>18} | {'ε_adapt':>15} | {'виклики f':>10}")
    print("-" * 70)

    for delta in [1e-4, 1e-6, 1e-8, 1e-10, 1e-12]:
        _call_count = 0
        I_adapt, max_depth = adaptive_simpson(a, b, delta)
        eps_adapt = abs(I_adapt - I_exact)
        print(f"{delta:>10.0e} | {I_adapt:>18.12f} | {eps_adapt:>15.6e} | {_call_count:>10}")

    print("\n" + "=" * 70)
    print("ПУНКТ 8: Порівняння результатів")
    print("=" * 70)

    print(f"\n{'Метод':<38} | {'Значення':>18} | {'Похибка':>15}")
    print("-" * 80)
    print(f"{'Точне значення':<38} | {I_exact:>18.12f} | {'0':>15}")
    print(f"{f'Сімпсон, N={N0}':<38} | {I_N0:>18.12f} | {eps_0:>15.6e}")
    print(f"{f'Сімпсон, N={N0//2}':<38} | {I_N0_half:>18.12f} | {abs(I_N0_half - I_exact):>15.6e}")
    print(f"{f'Сімпсон, N={N0//4}':<38} | {I_N0_quarter:>18.12f} | {abs(I_N0_quarter - I_exact):>15.6e}")
    print(f"{'Рунге-Ромберг':<38} | {I_RR:>18.12f} | {eps_RR:>15.6e}")
    print(f"{'Ейткен':<38} | {I_E:>18.12f} | {eps_E:>15.6e}")

    with open("epsilon_N.txt", "w") as file:
        file.write("# N epsilon\n")
        for N, eps in zip(Ns, epsilons):
            file.write(f"{N} {eps}\n")

    with open("comparison.txt", "w") as file:
        file.write("# method value error\n")
        file.write(f"exact {I_exact} 0\n")
        file.write(f"simpson_N0 {I_N0} {eps_0}\n")
        file.write(f"simpson_N0_2 {I_N0_half} {abs(I_N0_half - I_exact)}\n")
        file.write(f"simpson_N0_4 {I_N0_quarter} {abs(I_N0_quarter - I_exact)}\n")
        file.write(f"runge {I_RR} {eps_RR}\n")
        file.write(f"aitken {I_E} {eps_E}\n")

    print("\n→ epsilon_N.txt, comparison.txt")

    with open("plot_script.py", "w") as ps:
        ps.write("import matplotlib.pyplot as plt\n")
        ps.write("import numpy as np\n\n")

        ps.write("# Графік 1: f(x)\n")
        ps.write("x = np.linspace(0, 24, 1000)\n")
        ps.write("y = 50 + 20*np.sin(np.pi*x/12) + 5*np.exp(-0.2*(x-12)**2)\n")
        ps.write("plt.figure(figsize=(12, 5))\n")
        ps.write("plt.plot(x, y, 'b-', linewidth=2)\n")
        ps.write("plt.fill_between(x, 0, y, alpha=0.2)\n")
        ps.write("plt.xlabel('x')\n")
        ps.write("plt.ylabel('f(x)')\n")
        ps.write("plt.title('Навантаження на сервер f(x)')\n")
        ps.write("plt.grid(True, alpha=0.3)\n")
        ps.write("plt.tight_layout()\n")
        ps.write("plt.savefig('function.png', dpi=300)\n")
        ps.write("plt.close()\n\n")

        ps.write("# Графік 2: epsilon(N)\n")
        ps.write("data = np.loadtxt('epsilon_N.txt')\n")
        ps.write("plt.figure(figsize=(10, 6))\n")
        ps.write("plt.loglog(data[:, 0], data[:, 1], 'b-', linewidth=2)\n")
        ps.write("plt.xlabel('N')\n")
        ps.write("plt.ylabel('ε(N)')\n")
        ps.write("plt.title('Залежність похибки від N (Сімпсон)')\n")
        ps.write("plt.grid(True, which='both', alpha=0.3)\n")
        ps.write("plt.tight_layout()\n")
        ps.write("plt.savefig('epsilon_N.png', dpi=300)\n")
        ps.write("plt.close()\n\n")

        ps.write("print('Графіки: function.png, epsilon_N.png')\n")
        ps.write("plt.show()\n")

    print("→ plot_script.py")
    print("\nДля графіків: python3 plot_script.py")


if __name__ == "__main__":
    main()