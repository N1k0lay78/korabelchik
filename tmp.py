for age in range(1, 100):
    yo = ("год" if age % 10 == 1 else "года") if (5 > age % 10 > 0) and age // 10 != 1 else "лет"
    print(f"{age} {yo}")