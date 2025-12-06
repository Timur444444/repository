print("How old are you?: ")
age = int(input())

if age < 7:
     print("You can't play in computer")
elif age > 7 and age < 14:
     print("You can play for 1,5 hour")
elif age > 14 and age < 18:
     print("You can play for 3 hours")
else:
     print("You choose how long you spend on the computer")