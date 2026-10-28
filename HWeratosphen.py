n = input("Введите число N: ")

if not n.isdigit():
    print("Вы должны ввести целое число")
else:
    n = int(n)
    primes = {}

    for num in range(2, n + 1):
        is_prime = True

        for p in primes:
            if num % p == 0:
                is_prime = False
                break

        if is_prime:
            primes[num] = True
            print(num)