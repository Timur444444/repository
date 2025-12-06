def average(grades):
    """Возвращает среднее значение оценок."""
    return sum(grades) / len(grades)

subject = input("По какому предмету считаем оценки? ")

n = int(input("Сколько оценок нужно внести? "))

grades = []

for i in range(n):
    grade = int(input(f"Введите оценку №{i+1} (от 1 до 10): "))
    grades.append(grade)

avg = average(grades)

print(f"\nСредний балл по предмету '{subject}': {avg:.2f}")

if avg >= 8:
    print(f"Отлично по {subject}")
elif 5 <= avg <= 7:
    print(f"Неплохо, но можно лучше по {subject}")
else:
    print(f"Нужно подтянуть {subject}")
