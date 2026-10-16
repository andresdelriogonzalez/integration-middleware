import time

attempts = {"count": 0}


def flaky_hello():
    attempts["count"] += 1
    if attempts["count"] < 3:
        raise Exception(f"fallo simulado (intento {attempts['count']})")
    return "Hello, World"


for attempt in range(3):
    try:
        result = flaky_hello()
        print(f"Exito en el intento {attempt + 1}: {result}")
        break
    except Exception as e:
        print(f"Intento {attempt + 1} fallo: {e}")
        time.sleep(2 ** attempt)