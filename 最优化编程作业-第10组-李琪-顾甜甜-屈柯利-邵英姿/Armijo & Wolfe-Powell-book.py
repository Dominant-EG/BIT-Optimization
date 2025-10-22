import numpy as np


def rosenbrock(x):
    return 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2


def rosenbrock_grad(x):
    df_dx1 = -400 * x[0] * (x[1] - x[0] ** 2) - 2 * (1 - x[0])
    df_dx2 = 200 * (x[1] - x[0] ** 2)
    return np.array([df_dx1, df_dx2])


def armijo_search(f, grad_f, xk, pk, alpha0=1.0, rho=0.5, c1=1e-4, max_iter=100):
    print("Armijo方法搜索:")
    print("=" * 80)

    # 计算当前点的函数值和梯度
    fk = f(xk)
    gk = grad_f(xk)

    # 计算方向导数
    gk_pk = np.dot(gk, pk)

    history = []
    alpha = alpha0

    for i in range(max_iter):
        # 尝试新点
        x_new = xk + alpha * pk
        f_new = f(x_new)

        # Armijo条件: f(xk + alpha*pk) <= f(xk) + c1*alpha*gk^T*pk
        armijo_condition = f_new <= fk + c1 * alpha * gk_pk

        history.append({
            'iteration': i + 1,
            'alpha': alpha,
            'f_new': f_new,
            'armijo_condition': armijo_condition,
            'x_new': x_new.copy()
        })

        print(f"迭代 {i + 1:2d}: α = {alpha:.6f}, f(x+αp) = {f_new:.6f}, "
              f"Armijo条件: {armijo_condition}")

        if armijo_condition:
            print(f"Armijo条件满足，找到可接受步长 α = {alpha:.6f}")
            break
        else:
            # 收缩步长
            alpha = rho * alpha

    return alpha, history


def wolfe_powell_search(f, grad_f, xk, pk, mu=0.1, sigma=0.5, max_iter=100):
    print("Wolfe-Powell方法:")
    print("=" * 80)

    # 计算当前点的函数值和梯度
    fk = f(xk)
    gk = grad_f(xk)
    gk_pk = np.dot(gk, pk)

    # 初始化
    a = 0.0
    b = float('inf')
    alpha = 1.0
    j = 0

    history = []

    for j in range(max_iter):
        # Step 2: 计算新点
        x_new = xk + alpha * pk
        f_new = f(x_new)
        g_new = grad_f(x_new)
        g_new_pk = np.dot(g_new, pk)

        # 条件(3-1): Armijo条件 f(xk + αpk) ≤ f(xk) + μ*α*gk^T*pk
        condition1 = f_new <= fk + mu * alpha * gk_pk

        # 条件(3-2): 曲率条件 ∇f(xk + αpk)^T*pk ≥ σ*gk^T*pk
        condition2 = g_new_pk >= sigma * gk_pk

        history.append({
            'iteration': j + 1,
            'alpha': alpha,
            'x_new': x_new.copy(),
            'f_new': f_new,
            'condition1': condition1,
            'condition2': condition2,
            'a': a,
            'b': b
        })

        print(f"迭代 {j + 1}: α = {alpha:.6f}, f(x+αp) = {f_new:.6f}")
        print(f"        Armijo条件: {condition1}, 曲率条件: {condition2}")

        # 检查是否满足两个条件
        if condition1 and condition2:
            print(f"两个条件都满足，找到可接受步长 α = {alpha:.6f}")
            break

        # 如果不满足条件1，转Step 3
        if not condition1:
            print(f"        → 不满足Armijo条件，收缩区间")
            b = alpha
            alpha = (a + alpha) / 2
        # 如果满足条件1但不满足条件2，转Step 4
        elif condition1 and not condition2:
            print(f"        → 满足Armijo条件但不满足曲率条件，扩大区间")
            a = alpha
            if b == float('inf'):
                alpha = 2 * alpha
            else:
                alpha = min(2 * alpha, (alpha + b) / 2)

    return alpha, history


def main():
    # 初始点
    xk = np.array([0.0, 0.0])

    # 搜索方向
    pk = np.array([1.0, 0.0])

    print("问题描述:")
    print(f"目标函数: Rosenbrock函数")
    print(f"当前点 xk = {xk}")
    print(f"搜索方向 pk = {pk}")
    print(f"f(xk) = {rosenbrock(xk):.6f}")
    print(f"梯度 ∇f(xk) = {rosenbrock_grad(xk)}")
    print(f"方向导数 ∇f(xk)^T·pk = {np.dot(rosenbrock_grad(xk), pk):.6f}")
    print()

    # Armijo方法
    alpha_armijo, history_armijo = armijo_search(
        rosenbrock, rosenbrock_grad, xk, pk,
        alpha0=1.0, rho=0.5, c1=0.1, max_iter=20  # 使用μ=0.1作为c1
    )
    x_armijo = xk + alpha_armijo * pk
    print(f"Armijo方法: x_new = {x_armijo}, f(x_new) = {rosenbrock(x_armijo):.6f}")
    print( )

    # Wolfe-Powell方法
    alpha_wp, history_wp = wolfe_powell_search(
        rosenbrock, rosenbrock_grad, xk, pk,
        mu=0.1, sigma=0.5, max_iter=20
    )

    # 显示Wolfe-Powell迭代历史
    print("\nWolfe-Powell方法迭代历史:")
    print("-" * 100)
    print(f"{'迭代':<4} {'α':<10} {'f(x+αp)':<12} {'Armijo条件':<12} {'曲率条件':<12} {'a':<10} {'b':<10}")
    for step in history_wp:
        print(f"{step['iteration']:<4} {step['alpha']:<10.6f} {step['f_new']:<12.6f} "
              f"{step['condition1']:<12} {step['condition2']:<12} "
              f"{step['a']:<10.6f} {step['b']:<10.6f}")
    print(f"Wolfe-Powell方法找到的步长: α = {alpha_wp:.6f}")
    x_wp = xk + alpha_wp * pk
    print(f"Wolfe-Powell方法: x_new = {x_wp}, f(x_new) = {rosenbrock(x_wp):.6f}")


if __name__ == "__main__":
    main()