def get_total(price, quantity):
    """Функция возвращает стоимость одной позиции."""
    return price * quantity

n = int(input("Сколько разных видов сладостей хотите купить? "))

items = []

for i in range(n):
    print(f"\nСладость №{i+1}:")
    name = input("Название: ")
    price = float(input("Цена за 1 шт: "))
    quantity = int(input("Количество штук: "))
    
    items.append({
        "name": name,
        "price": price,
        "quantity": quantity
    })

total_sum = 0
for item in items:
    total_sum += get_total(item["price"], item["quantity"])

if total_sum >= 1000:
    discount_sum = total_sum * 0.9
    print(f"\nВам скидка 10%! Итоговая сумма: {discount_sum:.2f} руб.")
else:
    print(f"\nИтоговая сумма: {total_sum:.2f} руб. без скидки")
