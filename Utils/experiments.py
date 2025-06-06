import random
import time
import matplotlib.pyplot as plt
from Algorithm.genetic_algorithm import solve_with_genetic
from Algorithm.greedy_algorithm import solve_with_greedy
from Utils.data_handler import determine_region, AdLocation
def run_experiments():
    print("\n1. Визначення порогу стабільності (зупинка при відсутності покращень)")
    print("2. Вплив розмірності задачі на час та точність")
    choice = input("Виберіть експеримент (1, 2): ")
    if choice == '1':
        experiment_stop_by_stability()
    elif choice == '2':
        experiment_problem_size_vs_performance()
    else:
        print("Невірний вибір")

def experiment_stop_by_stability():  
    size = int(input("Введіть кількість локацій для експерименту: "))
    repeats = 500  # Кількість повторень

    thresholds = [20, 50, 100, 150, 200, 300, 500]
    results = []

    for threshold in thresholds:
        total_coverage = 0
        total_iterations = 0

        for _ in range(repeats):
            data, constraints = generate_random_data_with_size(size)
            best, used_generations = solve_with_genetic(
                data, constraints,
                generations=3000,
                patience=threshold
            )
            total_coverage += best.total_coverage
            total_iterations += used_generations

        avg_coverage = total_coverage / repeats
        avg_iterations = total_iterations / repeats

        print(f"Поріг стабільності: {threshold} → Середнє покриття: {avg_coverage:.2f}")
        results.append((threshold, avg_iterations, avg_coverage))

    plt.figure(figsize=(10, 4))

    # Графік покриття
    plt.subplot(1, 2, 1)
    plt.plot([r[0] for r in results], [r[2] for r in results], marker='o', label='Середнє покриття')
    plt.title("Покриття vs Поріг стабільності")
    plt.xlabel("Ітерацій без покращення")
    plt.ylabel("Середнє покриття")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()




def generate_random_data_with_size(n):
    center_x, center_y = 50, 50
    data = []
    for _ in range(n):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        price = random.randint(1, 500)
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
    return data, constraints

def experiment_problem_size_vs_performance():
    sizes = [10, 30, 50, 70, 100]
    generations = [300, 700, 1000, 2000, 5000]
    repeats = 100

    times_genetic = []
    coverages_genetic = []
    times_greedy = []
    coverages_greedy = []

    for i, size in enumerate(sizes):
        total_time_genetic = 0
        total_coverage_genetic = 0
        total_time_greedy = 0
        total_coverage_greedy = 0
    

        for _ in range(repeats):
            data_sample, constraints = generate_random_data_with_size(size)

            start = time.time()
            best, _ = solve_with_genetic(data_sample, constraints, generations[i])
            end = time.time()

            total_time_genetic += (end - start)
            total_coverage_genetic += best.total_coverage

            start = time.time()
            greedy_result = solve_with_greedy(data_sample, constraints)
            end = time.time()
            total_time_greedy += (end - start)
            total_coverage_greedy += greedy_result["coverage"]

        avg_time_genetic = total_time_genetic / repeats
        avg_coverage_genetic = total_coverage_genetic / repeats
        avg_time_greedy = total_time_greedy / repeats
        avg_coverage_greedy = total_coverage_greedy / repeats

        times_genetic.append(avg_time_genetic)
        coverages_genetic.append(avg_coverage_genetic)
        times_greedy.append(avg_time_greedy)
        coverages_greedy.append(avg_coverage_greedy)

        print(f"{size} локацій → Генетичний: {avg_coverage_genetic:.2f} покриття, {avg_time_genetic:.2f} сек")
        print(f"{size} локацій → Жадібний: {avg_coverage_greedy:.2f} покриття, {avg_time_greedy:.2f} сек")

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Кількість локацій')
    ax1.set_ylabel('Час (сек)', color='tab:red')
    ax1.plot(sizes, times_genetic, 'r-o', label='Генетичний')
    ax1.plot(sizes, times_greedy, 'r--', label='Жадібний')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Покриття', color='tab:blue')
    ax2.plot(sizes, coverages_genetic, 'b-s', label='Генетичний')
    ax2.plot(sizes, coverages_greedy, 'b--', label='Жадібний')
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.legend(loc='upper right')

    plt.title("Вплив розмірності задачі на час та покриття (усереднено)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
