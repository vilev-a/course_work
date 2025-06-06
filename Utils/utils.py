import json


def print_locations(data):
    print("\nЛокації:")
    for i, loc in enumerate(data):
        print(f"{i+1}. ({loc.x}, {loc.y}) | Ціна: {loc.price}, Покриття: {loc.coverage}, Регіон: {loc.location}")

def save_results_to_file(filename, best_genetic, best_greedy):
    result = {
        "genetic": {
            "totalCoverage": best_genetic.total_coverage,
            "totalPrice": best_genetic.total_price,
            "regions": best_genetic.region_prices,
            "genes": best_genetic.gens,
        },
        "greedy": {
            "totalCoverage": best_greedy['coverage'],
            "totalPrice": best_greedy['price'],
            "locations": [
                {
                    "x": loc.x,
                    "y": loc.y,
                    "price": loc.price,
                    "coverage": loc.coverage,
                    "region": loc.location
                } for loc in best_greedy['locations']
            ]
        }
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Результати збережено у файл: {filename}")