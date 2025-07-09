
pi =  3.141592653589793 # Variable global

def suma(a: int, b:int) -> int:
    return a + b

def resta(a: int, b:int) -> int:
    return suma(a,-b)

if __name__ == "__main__":
    import sys
    resultado = suma(int(sys.argv[1]), int(sys.argv[2]))
    print(resultado)