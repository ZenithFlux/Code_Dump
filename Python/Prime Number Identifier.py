from math import sqrt

class prime_identifier:
    def __init__(self,n):
        i=0
        if n<2 or n%1!=0:
            raise ValueError("value should neither be a decimal nor less than than 2")
        else:
            is_prime = True
            if n in (2, 3, 5):
                None
            elif n%2==0:
                is_prime=False
                i=2
            elif n%3==0:
                is_prime = False
                i=3
            elif n%5==0:
                is_prime = False
                i=5
            elif sqrt(n)%1==0:
                is_prime = False
                i = int(sqrt(n))
            else:
                i=7
                while i<sqrt(n):
                    if str(i)[-1] != 5:
                        if n%i==0:
                            is_prime = False
                            break
                        else:
                            i+=2
                            continue
                    else:
                        i+=2
            self.is_prime= is_prime
            self.multiple = i

print("This program checks weather a number is prime number or not.")
while True:
    try:
        n=int(input("Enter a whole number: "))
    except:
        print("This is an invalid input. No input accepted except 0-9 digits.")
        continue
    if n==1:
        print("1 is neither a prime nor a composite number.")
        continue
    elif n<=0:
        print("Please enter a number larger than 0,")
        continue
    else:
        p= prime_identifier(n)

        if p.is_prime:
            print(str(n)+" is a prime number.")
        else:
            print(str(n)+" is not a prime number as it is at least divisible by "+str(p.multiple)+".")
