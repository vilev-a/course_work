import sys
from Utils.data_handler import load_data_manual, load_data_file, generate_random_data
from Utils.experiments import run_experiments
from Algorithm.genetic_algorithm import solve_with_genetic
from Algorithm.greedy_algorithm import solve_with_greedy
from Utils.utils import print_locations, save_results_to_file

# Глобальні змінні
data = []
constraints = {}

def main_menu():
    global data, constraints

    while True:
        print("\n--- ГОЛОВНЕ МЕНЮ ---")
        print("1. Внести дані задачі")
        print("2. Розв'язати задачу")
        print("3. Провести експерименти")
        print("4. Вивести дані задачі")
        print("5. Завершити роботу")
        choice = input("Виберіть пункт: ")

        if choice == '1':
            print("\n1. Вручну")
            print("2. Зчитати з файлу")
            print("3. Згенерувати випадкові дані")
            sub_choice = input("Виберіть спосіб введення: ")

            try:
                center_x = int(input("Введіть координату центру X: "))
                center_y = int(input("Введіть координату центру Y: "))
                if not (0 <= center_x <= 100 and 0 <= center_y <= 100):
                    print("Координати мають бути в межах від 0 до 100.")
                    continue
            except ValueError:
                print("Координати мають бути цілими числами.")
                continue

            if sub_choice == '1':
                data, constraints = load_data_manual(center_x, center_y)
            elif sub_choice == '2':
                data, constraints = load_data_file(center_x, center_y)
            elif sub_choice == '3':
                data, constraints = generate_random_data(center_x, center_y)
            else:
                print("Невірний вибір")

        elif choice == '2':
            if not data:
                print("Спочатку потрібно внести дані")
                continue

            best_greedy = solve_with_greedy(data, constraints)
            generations = int(input("Введіть кількість поколінь генетичного алгоритму: "))
            best_genetic, _ = solve_with_genetic(data, constraints, generations)

            best_genetic.region_prices = {
                'north-west': best_genetic.north_west_price,
                'north-east': best_genetic.north_east_price,
                'south-west': best_genetic.south_west_price,
                'south-east': best_genetic.south_east_price,
            }

            while True:
                print("\nЩо зробити з результатами?")
                print("1. Вивести у консоль")
                print("2. Зберегти у файл")
                print("3. Повернутися до головного меню")
                res_choice = input("Оберіть опцію: ")

                if res_choice == '1':
                    # Вивід у консоль
                    print("\n--- Результати жадібного алгоритму ---")
                    print(f"Покриття: {best_greedy['coverage']}")
                    print(f"Ціна: {best_greedy['price']}")
                    print("Вибрані локації:")
                    for loc in best_greedy['locations']:
                        print(f"  Координати: ({loc.x}, {loc.y}), Ціна: {loc.price}, Покриття: {loc.coverage}, Регіон: {loc.location}")

                    print("\n--- Результати генетичного алгоритму ---")
                    print(f"Покриття: {best_genetic.total_coverage}")
                    print(f"Ціна: {best_genetic.total_price}")
                    print(f"Ціна по регіонах: {best_genetic.region_prices}")
                    print(f"Гени: {best_genetic.gens}")

                elif res_choice == '2':
                    # Збереження у файл
                    filepath = input("Введіть шлях до файлу (або натисніть Enter для 'results.json'): ").strip()
                    if filepath == '':
                        filepath = 'results.json'

                    save_results_to_file(filepath, best_genetic, best_greedy)
                    print(f"Результати збережено у файл: {filepath}")

                elif res_choice == '3':
                    break
                else:
                    print("Невірний вибір, спробуйте ще раз.")


        elif choice == '3':
            run_experiments()

        elif choice == '4':
            print_locations(data)
            print("Обмеження:", constraints)

        elif choice == '5':
            print("Завершення програми...")
            sys.exit()
        else:
            print("Невірний вибір")

if __name__ == '__main__':
    main_menu()
