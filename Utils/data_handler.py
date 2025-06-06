import json
import random

class AdLocation:
    def __init__(self, x, y, price, coverage, location):
        self.x = x
        self.y = y
        self.price = price
        self.coverage = coverage
        self.location = location

def validate_input(value, min_val, max_val, prompt):
    """Універсальна функція для валідації вводу"""
    while True:
        try:
            num = int(input(prompt))
            if min_val <= num <= max_val:
                return num
            print(f"Значення має бути від {min_val} до {max_val}!")
        except ValueError:
            print("Будь ласка, введіть ціле число!")

def determine_region(x, y, center_x, center_y):
    if y >= center_y and x <= center_x:
        return 'north-west'
    elif y >= center_y and x > center_x:
        return 'north-east'
    elif y < center_y and x <= center_x:
        return 'south-west'
    else:
        return 'south-east'

def load_data_manual(center_x, center_y):
    data = []
    n = validate_input(0, 1, 1000, "Кількість локацій (1-1000): ")
    
    for i in range(n):
        print(f"\nЛокація {i+1}:")
        x = validate_input(0, 0, 100, "  x (0-100): ")
        y = validate_input(0, 0, 100, "  y (0-100): ")
        price = validate_input(0, 1, 10000, "  price (≥1): ")
        coverage = validate_input(0, 1, 10000, "  coverage (≥1): ")
        region = determine_region(x, y, center_x, center_y)
        data.append(AdLocation(x, y, price, coverage, region))

    print("\nВведіть обмеження:")
    constraints = {
        "maxTotalPrice": validate_input(0, 1, 100000, "maxTotalPrice (≥1): "),
        "maxNorthWestRegionPrice": validate_input(0, 0, 100000, "maxNorthWestRegionPrice (≥0): "),
        "maxNorthEastRegionPrice": validate_input(0, 0, 100000, "maxNorthEastRegionPrice (≥0): "),
        "maxSouthWestRegionPrice": validate_input(0, 0, 100000, "maxSouthWestRegionPrice (≥0): "),
        "maxSouthEastRegionPrice": validate_input(0, 0, 100000, "maxSouthEastRegionPrice (≥0): "),
    }
    return data, constraints

def load_data_file(center_x, center_y):
    filename = input("Введіть шлях до JSON-файлу з даними: ")
    try:
        with open(filename, 'r') as f:
            raw = json.load(f)
        
        # Валідація даних з файлу
        for loc in raw['locations']:
            if not (0 <= loc['x'] <= 100 and 0 <= loc['y'] <= 100):
                raise ValueError("Координати повинні бути від 0 до 100")
            if loc['price'] < 0 or loc['coverage'] < 0:
                raise ValueError("Ціна та покриття не можуть бути від'ємними")
                
        data = [
            AdLocation(loc['x'], loc['y'], loc['price'], loc['coverage'],
            determine_region(loc['x'], loc['y'], center_x, center_y))
            for loc in raw['locations']
        ]
        
        # Валідація обмежень
        for key in ['maxTotalPrice', 'maxNorthWestRegionPrice', 'maxNorthEastRegionPrice',
                   'maxSouthWestRegionPrice', 'maxSouthEastRegionPrice']:
            if raw['constraints'][key] < 0:
                raise ValueError(f"Обмеження {key} не може бути від'ємним")
                
        constraints = raw['constraints']
        return data, constraints
        
    except Exception as e:
        print(f"Помилка при завантаженні файлу: {e}")
        return [], {}

def generate_random_data(center_x, center_y):
    n = validate_input(0, 1, 1000, "Кількість локацій для генерації (1-1000): ")
    data = []
    
    for _ in range(n):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        price = random.randint(1, 300)
        coverage = random.randint(10, 1000)
        region = determine_region(x, y, center_x, center_y)
        data.append(AdLocation(x, y, price, coverage, region))

    constraints = {
        "maxTotalPrice": random.randint(500, 3000),
        "maxNorthWestRegionPrice": random.randint(200, 1000),
        "maxNorthEastRegionPrice": random.randint(200, 1000),
        "maxSouthWestRegionPrice": random.randint(200, 1000),
        "maxSouthEastRegionPrice": random.randint(200, 1000),
    }
    
    print("\nЗгенеровані обмеження:")
    for key, value in constraints.items():
        print(f"{key}: {value}")
        
    return data, constraints