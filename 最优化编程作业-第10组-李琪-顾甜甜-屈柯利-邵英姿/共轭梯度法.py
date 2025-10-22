import numpy as np


def conjugate_gradient(A, b, x0, max_iter=100, tol=1e-6):
    x = x0.copy()
    r = b - A @ x  # 初始残差
    p = r.copy()  # 初始搜索方向
    iterations = [x.copy()]

    for k in range(max_iter):
        Ap = A @ p
        alpha = np.dot(r, r) / np.dot(p, Ap)
        x = x + alpha * p
        r_new = r - alpha * Ap

        # 检查收敛
        if np.linalg.norm(r_new) < tol:
            iterations.append(x.copy())
            break

        beta = np.dot(r_new, r_new) / np.dot(r, r)
        p = r_new + beta * p
        r = r_new
        iterations.append(x.copy())

    return x, iterations


def problem1():
    """求解第一个问题: min 1/2*x1^2 + x2^2"""
    print("=" * 50)
    print("问题1: min 1/2*x1^2 + x2^2")
    print("=" * 50)

    # 将问题转化为二次型: f(x) = 1/2 * x^T A x
    # 其中 A = [[1, 0], [0, 2]]
    A = np.array([[1, 0],
                  [0, 2]], dtype=float)

    # 对于无约束极小化问题 min 1/2*x^T A x，最优解是 Ax = 0 的解
    b = np.array([0, 0], dtype=float)
    x0 = np.array([4, 4], dtype=float)

    print(f"初始点: x0 = {x0}")
    print(f"系数矩阵 A:\n{A}")

    x_opt, iterations = conjugate_gradient(A, b, x0)

    print(f"\n最优解: x* = {x_opt}")
    print(f"目标函数值: f(x*) = {0.5 * x_opt[0] ** 2 + x_opt[1] ** 2}")

    print(f"\n迭代过程:")
    for i, x in enumerate(iterations):
        print(f"迭代 {i}: x = {x}, f(x) = {0.5 * x[0] ** 2 + x[1] ** 2:.6f}")

    return x_opt, iterations


def problem2():
    """求解第二个问题: min 2x1^2 + 2x1x2 + 5x2^2"""
    print("\n" + "=" * 50)
    print("问题2: min 2x1^2 + 2x1x2 + 5x2^2")
    print("=" * 50)

    # 将问题转化为二次型: f(x) = 1/2 * x^T A x
    # f(x) = 2x1^2 + 2x1x2 + 5x2^2 = 1/2 * x^T [[4, 2], [2, 10]] x
    A = np.array([[4, 2],
                  [2, 10]], dtype=float)

    b = np.array([0, 0], dtype=float)
    x0 = np.array([2, -2], dtype=float)

    print(f"初始点: x0 = {x0}")
    print(f"系数矩阵 A:\n{A}")

    x_opt, iterations = conjugate_gradient(A, b, x0)

    print(f"\n最优解: x* = {x_opt}")
    print(f"目标函数值: f(x*) = {2 * x_opt[0] ** 2 + 2 * x_opt[0] * x_opt[1] + 5 * x_opt[1] ** 2}")

    print(f"\n迭代过程:")
    for i, x in enumerate(iterations):
        print(f"迭代 {i}: x = {x}, f(x) = {2 * x[0] ** 2 + 2 * x[0] * x[1] + 5 * x[1] ** 2:.6f}")

    return x_opt, iterations



if __name__ == "__main__":
    # 求解问题1
    x_opt1, iter1 = problem1()

    # 求解问题2
    x_opt2, iter2 = problem2()

  