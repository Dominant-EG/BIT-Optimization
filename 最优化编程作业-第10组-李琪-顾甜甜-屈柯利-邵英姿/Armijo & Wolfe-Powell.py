import numpy as np


def rosenbrock(x):
    return 100 * (x[1] - x[0] ** 2) ** 2 + (1 - x[0]) ** 2


def rosenbrock_grad(x):
    df_dx1 = -400 * x[0] * (x[1] - x[0] ** 2) - 2 * (1 - x[0])
    df_dx2 = 200 * (x[1] - x[0] ** 2)
    return np.array([df_dx1, df_dx2])


def armijo_search(f, grad_f, xk, pk, alpha0=1.0, rho=0.6, c1=1e-4, max_iter=100):
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


def wolfe_powell_search(f, grad_f, xk, pk, beta=1.0, rho=0.5, c1=1e-4, c2=0.9, max_iter=100):
    print("Wolfe-Powell方法:")
    print("=" * 80)

    # 计算当前点的函数值和梯度
    fk = f(xk)
    gk = grad_f(xk)
    gk_pk = np.dot(gk, pk)

    history = []

    # Step 0: 检查α=1是否满足条件
    alpha_test = 1.0
    x_test = xk + alpha_test * pk
    f_test = f(x_test)
    g_test = grad_f(x_test)
    g_test_pk = np.dot(g_test, pk)

    # Armijo条件: f(xk + αpk) ≤ f(xk) + c1*α*gk^T*pk
    armijo_cond = f_test <= fk + c1 * alpha_test * gk_pk
    # 曲率条件: ∇f(xk + αpk)^T*pk ≥ c2*gk^T*pk
    curvature_cond = g_test_pk >= c2 * gk_pk

    history.append({
        'step': 'Step 0',
        'alpha': alpha_test,
        'f_new': f_test,
        'armijo': armijo_cond,
        'curvature': curvature_cond,
        'both_conditions': armijo_cond and curvature_cond
    })

    print(f"Step 0: 测试 α = {alpha_test:.6f}")
    print(f"        f(x+αp) = {f_test:.6f}, Armijo条件: {armijo_cond}, 曲率条件: {curvature_cond}")

    if armijo_cond and curvature_cond:
        print("        α=1 满足条件，返回 α = 1.0")
        return alpha_test, history

    # Step 1: 在集合 {βρ^i} 中找到满足Armijo条件的最大α
    print(f"\nStep 1: 在集合 {{βρ^i}} = {{{beta}*{rho}^i}} 中寻找满足Armijo条件的最大α")

    # 生成候选步长集合
    candidates = []
    for i in range(0, 10):  # 正向搜索
        alpha_candidate = beta * (rho ** (-i))
        x_candidate = xk + alpha_candidate * pk
        f_candidate = f(x_candidate)
        armijo_candidate = f_candidate <= fk + c1 * alpha_candidate * gk_pk
        candidates.append((alpha_candidate, f_candidate, armijo_candidate))

        if alpha_candidate > 100:  # 防止步长过大
            break

    for i in range(1, 10):  # 负向搜索
        alpha_candidate = beta * (rho ** i)
        x_candidate = xk + alpha_candidate * pk
        f_candidate = f(x_candidate)
        armijo_candidate = f_candidate <= fk + c1 * alpha_candidate * gk_pk
        candidates.append((alpha_candidate, f_candidate, armijo_candidate))

    # 找到满足Armijo条件的最大α
    alpha0 = 0.0
    for alpha_candidate, f_candidate, armijo_candidate in sorted(candidates, reverse=True):
        if armijo_candidate:
            alpha0 = alpha_candidate
            break

    if alpha0 == 0.0:
        alpha0 = min(candidates, key=lambda x: x[1])[0]  # 选择函数值最小的

    history.append({
        'step': 'Step 1',
        'alpha': alpha0,
        'f_new': f(xk + alpha0 * pk),
        'armijo': True,
        'curvature': '待检验',
        'both_conditions': False
    })

    print(f"        找到 α⁽⁰⁾ = {alpha0:.6f}")

    # 主循环
    alpha_i = alpha0
    for i in range(max_iter):
        print(f"\nStep 2 (i={i}): 检验 α⁽{i}⁾ = {alpha_i:.6f} 是否满足曲率条件")

        # 计算当前点的梯度信息
        x_current = xk + alpha_i * pk
        g_current = grad_f(x_current)
        g_current_pk = np.dot(g_current, pk)
        curvature_cond = g_current_pk >= c2 * gk_pk

        history.append({
            'step': f'Step 2 (i={i})',
            'alpha': alpha_i,
            'f_new': f(x_current),
            'armijo': True,
            'curvature': curvature_cond,
            'both_conditions': curvature_cond
        })

        print(f"        ∇f(x+αp)^T·p = {g_current_pk:.6f}, c2*∇f(x)^T·p = {c2 * gk_pk:.6f}")
        print(f"        曲率条件: {curvature_cond}")

        if curvature_cond:
            print(f"        α⁽{i}⁾ 满足所有条件，返回 α = {alpha_i:.6f}")
            return alpha_i, history

        # Step 3: 插值求新的α
        beta_i = alpha_i / rho

        print(f"Step 3 (i={i}): β⁽{i}⁾ = {beta_i:.6f}")
        print(f"        在区间 [α⁽{i}⁾, β⁽{i}⁾] = [{alpha_i:.6f}, {beta_i:.6f}] 中插值搜索")

        # 收集区间内的候选点进行插值
        best_alpha = alpha_i
        best_f = f(xk + alpha_i * pk)

        # 在区间内生成插值点
        for j in range(10):
            # 线性插值点
            alpha_candidate = alpha_i + (rho ** j) * (beta_i - alpha_i)

            if alpha_candidate > beta_i:
                break

            x_candidate = xk + alpha_candidate * pk
            f_candidate = f(x_candidate)

            # 检查Armijo条件
            armijo_candidate = f_candidate <= fk + c1 * alpha_candidate * gk_pk

            if armijo_candidate and f_candidate < best_f:
                best_alpha = alpha_candidate
                best_f = f_candidate

        alpha_next = best_alpha

        history.append({
            'step': f'Step 3 (i={i})',
            'alpha': alpha_next,
            'f_new': best_f,
            'armijo': True,
            'curvature': '待检验',
            'both_conditions': False
        })

        print(f"        找到新的 α⁽{i + 1}⁾ = {alpha_next:.6f}")

        alpha_i = alpha_next

    print("达到最大迭代次数，返回当前最佳步长")
    return alpha_i, history


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
        alpha0=1.0, rho=0.6, c1=1e-4, max_iter=20
    )

    # 计算Armijo方法的新点
    x_armijo = xk + alpha_armijo * pk
    print(f"Armijo方法: x_new = {x_armijo}, f(x_new) = {rosenbrock(x_armijo):.6f}")
    print()

    # Wolfe-Powell方法
    alpha_wp, history_wp = wolfe_powell_search(
        rosenbrock, rosenbrock_grad, xk, pk,
        beta=1.0, rho=0.5, c1=1e-4, c2=0.9, max_iter=10
    )

    # 显示迭代历史
    print("Wolfe-Powell方法迭代历史:")
    print("-" * 80)
    for step in history_wp:
        print(f"{step['step']:12} | α = {step['alpha']:8.6f} | f = {step['f_new']:10.6f} | "
              f"Armijo: {step['armijo']:5} | Curvature: {step['curvature']:5}")

    print(f"Wolfe-Powell方法找到的步长: α = {alpha_wp:.6f}")

    #计算Wolfe-Powell方法的新点
    x_wp = xk + alpha_wp * pk
    print(f"Wolfe-Powell方法: x_new = {x_wp}, f(x_new) = {rosenbrock(x_wp):.6f}")


if __name__ == "__main__":
    main()