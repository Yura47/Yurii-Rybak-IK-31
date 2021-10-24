print("First constant", False)
print("Second constant", True)
print("None constant", None)

print(abs(-10.11), f" {abs(10.11)}")
print(bin(1234))
print(float('+5.67'))

B = True
print("So B=True" if B else " So B=False")
B = Falsenaz
print("So B=True" if B else " So B=False")

try:
    a = int(input("the first number: "))
    b = int(input("the second number: "))
    print (a / b)
except (ValueError, ZeroDivisionError):
    print("Error...")
finally:
    print("THE END).")


with open("README.md", "r") as f:
	for line in f :
		print(line)
		

full_name = lambda first, last: f'Full name{first} {last}'
full_name('Yurii','Rybak')
print("Simple function", full_name)
print("Call function", full_name ('Yurii', 'Rybak'))
