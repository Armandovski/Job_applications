def menor_inteiro(numero):
	from math import gcd

	lcm = numero[0]

	for i in numero[1:]:
		lcm = lcm*i//gcd(lcm,i)

	return lcm

def main():
	value = menor_inteiro([1, 2, 3, 4, 5, 6, 7, 8, 9])

	print(value)
	return

if __name__ == '__main__':
	main()
