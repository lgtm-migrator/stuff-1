def area_perimeter(shape, pi):
    if "circle" in shape:
        radius = float(input("Circle radius\n> "))
        area = pi * pow(radius, 2)
        perimeter = 2 * pi * radius
    elif "triangle" in shape:
        base = float(input("Triangle base\n> "))
        height = float(input("Triangle height\n> "))
        area = 0.5 * base * height
        side = float(input("Side of triangle\n> "))
        side_ = float(input("Other side of triangle\n> "))
        perimeter = base + side + side_
    elif "square" in shape:
        side = float(input("Side of square\n> "))
        area = pow(side, 2)
        perimeter = 4 * side
    elif "rectangle" in shape:
        side = float(input("Rectangle width\n> "))
        side_ = float(input("Rectangle height\n> "))
        area = side * side_
        perimeter = 2 * (side + side_)
    return area, perimeter


def choice(number, shape_list):
    if number == 1:
        shape = shape_list[0]
    elif number == 2:
        shape = shape_list[1]
    elif number == 3:
        shape = shape_list[2]
    elif number == 4:
        shape = shape_list[3]
    return shape


def main():
    count = 0
    shape_list = ["circle", "triangle", "square", "rectangle"]
    for shape in shape_list:
        count += 1
        print(f"{count}. {shape.title()}")
    shape_choice = choice(int(input("> ")), shape_list)
    shape_result = area_perimeter(shape_choice, 3.14)
    string = f"{shape_choice.title()}\nArea = {shape_result[0]}\nPerimeter = {shape_result[1]}"
    print(string)


if __name__ == "__main__":
    main()
