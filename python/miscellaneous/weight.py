def weight_convert(weight, unit):
    if unit.upper() == "L":
        final_weight = weight * 0.45
        unit = "kilos"
    elif unit.upper() == "K":
        final_weight = weight // 0.45
        unit = "pounds"
    output = f"You are {final_weight} {unit}"
    return output


if __name__ == "__main__":
    weight = int(input("Weight: "))
    unit = input("(L)bs or (K)gs: ")
    print(weight_convert(weight, unit))
