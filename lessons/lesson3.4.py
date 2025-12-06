#Создать функцию которая будет спрашивать у пользователей имя фамилию и возраст потом выведет это в консоль

def user():
     name = input("Your name: ")
     surname = input("Your surname: ")
     age = input("Your age: ")
     print(name, surname, age)
user()


NSA = input("Are you registed?")
if NSA == "not":
    name = input("Your name: ")
    surname = input("Your surname: ")
    age = input("Your age: ")
    print(name, surname, age)
else:
    print("You are registed")   