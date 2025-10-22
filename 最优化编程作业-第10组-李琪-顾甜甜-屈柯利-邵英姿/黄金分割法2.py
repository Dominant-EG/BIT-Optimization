import math


def golden_section_search(f, a, b, tol=1e-4, max_iter=100):

    # 黄金分割比例
    golden_ratio = (math.sqrt(5) - 1) / 2

    # 初始点
    x1 = b - golden_ratio * (b - a)
    x2 = a + golden_ratio * (b - a)

    f1 = f(x1)
    f2 = f(x2)

    history = []

    for i in range(max_iter):
        # 记录当前状态
        history.append({
            'iteration': i + 1,
            'a': a,
            'b': b,
            'x1': x1,
            'x2': x2,
            'f1': f1,
            'f2': f2,
            'interval_length': b - a
        })

        # 检查收敛条件
        if abs(b - a) < tol:
            break

        if f1 < f2:
            # 最小值在 [a, x2] 区间
            b = x2
            x2 = x1
            f2 = f1
            x1 = b - golden_ratio * (b - a)
            f1 = f(x1)
        else:
            # 最小值在 [x1, b] 区间
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + golden_ratio * (b - a)
            f2 = f(x2)

    # 最终结果
    x_min = (a + b) / 2
    f_min = f(x_min)

    return x_min, f_min, history


def f12(x):
    return math.exp(-x) + x**2


def main():
    # 设置参数
    a = -1.0  # 区间左端点
    b = 1.0  # 区间右端点
    tol = 1e-4  # 精度要求

    print("黄金分割法求解 f12(x) = e^(-x) - 2x + 1 的最小值")
    print(f"初始区间: [{a}, {b}]")
    print(f"精度要求: {tol}")
    print("=" * 80)

    # 执行黄金分割法
    x_min, f_min, history = golden_section_search(f12, a, b, tol)

    # 打印迭代过程
    print("迭代过程:")
    print(f"{'迭代次数':<8} {'a':<12} {'b':<12} {'x1':<12} {'x2':<12} {'f(x1)':<12} {'f(x2)':<12} {'区间长度':<12}")
    print("-" * 100)

    for step in history:
        print(f"{step['iteration']:<8} {step['a']:<12.6f} {step['b']:<12.6f} "
              f"{step['x1']:<12.6f} {step['x2']:<12.6f} "
              f"{step['f1']:<12.6f} {step['f2']:<12.6f} "
              f"{step['interval_length']:<12.6f}")

    print("=" * 80)
    print("最终结果:")
    print(f"最小值点 x* = {x_min:.8f}")
    print(f"最小值 f(x*) = {f_min:.8f}")
    print(f"实际迭代次数: {len(history)}")


if __name__ == "__main__":
    main()