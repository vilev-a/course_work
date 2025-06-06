import random
from dataclasses import dataclass
from typing import List, Dict

# === Класи ===

@dataclass
class AdLocation:
    x: int
    y: int
    price: int
    coverage: int
    location: str  # 'north-west', 'north-east', 'south-west', 'south-east'


@dataclass
class PopulationCandidate:
    total_price: int
    north_west_price: int
    north_east_price: int
    south_west_price: int
    south_east_price: int
    total_coverage: int
    gens: List[int]


# === Допоміжні функції ===


def get_flattened_locations(locations_object: Dict[str, List[AdLocation]]) -> List[AdLocation]:
    return locations_object['north-west'] + locations_object['north-east'] + \
           locations_object['south-west'] + locations_object['south-east']



def satisfies_constraints(candidate: PopulationCandidate, constraints: Dict) -> bool:
    return (candidate.total_price <= constraints['maxTotalPrice'] and
            candidate.north_west_price <= constraints['maxNorthWestRegionPrice'] and
            candidate.north_east_price <= constraints['maxNorthEastRegionPrice'] and
            candidate.south_west_price <= constraints['maxSouthWestRegionPrice'] and
            candidate.south_east_price <= constraints['maxSouthEastRegionPrice'] and
            candidate.total_coverage > 0)


def get_evaluated_candidate(gens: List[int], all_locations: List[AdLocation]) -> PopulationCandidate:
    total_price = total_coverage = 0
    nw = ne = sw = se = 0

    for gene, loc in zip(gens, all_locations):
        if gene:
            total_price += loc.price
            total_coverage += loc.coverage
            if loc.location == 'north-west':
                nw += loc.price
            elif loc.location == 'north-east':
                ne += loc.price
            elif loc.location == 'south-west':
                sw += loc.price
            elif loc.location == 'south-east':
                se += loc.price

    return PopulationCandidate(
        total_price, nw, ne, sw, se, total_coverage, gens
    )


def get_region_cost(region_genes, region_locations):
    return sum(loc.price for i, loc in enumerate(region_locations) if region_genes[i] == 1)

def satisfies_region_constraints(region_code, region_cost, constraints):
    return region_cost <= constraints[f'max{region_code.title().replace("-", "")}RegionPrice']

def generate_region_locations(region_code, region_locations, current_total, constraints):
    region_size = len(region_locations)
    if region_size == 0:
        return [0] * 0, 0  # Порожній регіон

    genes = [0] * region_size
    region_cost = 0
    attempts = 0
    max_attempts = 2 ** region_size
    added_index = None
    max_failures = 30  # Кількість невдалих спроб, після яких зупиняємося
    failures = 0


    while attempts < max_attempts and failures < max_failures:
        if all(gene == 1 for gene in genes):
            break  # Всі локації вже вибрані

        idx = random.randint(0, region_size - 1)
        if genes[idx] == 1:
            continue
        genes[idx] = 1
        region_cost = get_region_cost(genes, region_locations)

        if not satisfies_region_constraints(region_code, region_cost, constraints) or \
           (current_total + region_cost > constraints['maxTotalPrice']):
            genes[idx] = 0
            failures += 1
        else:
            attempts += 1



    if added_index is not None and (current_total + region_cost > constraints['maxTotalPrice']):
        genes[added_index] = 0

    return genes, get_region_cost(genes, region_locations)


def generate_initial_population(locations_object, constraints) -> List[PopulationCandidate]:
    initial_population = []
    region_codes = list(locations_object.keys())

    for shift in range(len(region_codes)):
        for _ in range(2 ** len(region_codes)):
            total_cost = 0
            gens_per_region = {}
            for region in region_codes:
                region_gens, region_cost = generate_region_locations(
                                                                        region,
                                                                        locations_object[region],
                                                                        total_cost,
                                                                        constraints
                                                                    )

                gens_per_region[region] = region_gens
                total_cost += region_cost

            full_gens = gens_per_region['north-west'] + gens_per_region['north-east'] + \
                        gens_per_region['south-west'] + gens_per_region['south-east']
            flat_locations = get_flattened_locations(locations_object)
            candidate = get_evaluated_candidate(full_gens, flat_locations)
            initial_population.append(candidate)

        # циклічний зсув
        region_codes = region_codes[1:] + [region_codes[0]]

    return sorted(initial_population, key=lambda c: c.total_coverage, reverse=True)


def mutate(genes: List[int], mutation_rate: float = 0.05) -> List[int]:
    mutated = genes[:]
    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            mutated[i] = 1 - mutated[i]  # інверсія гена
    return mutated



def genetic_crossing(c1: PopulationCandidate, c2: PopulationCandidate,
                     all_locations: List[AdLocation], mutation_chance: int = 5) -> PopulationCandidate:
    point = random.randint(0, len(c1.gens) - 1)
    new_gens = c1.gens[:point] + c2.gens[point:]

    if random.randint(1, 100) <= mutation_chance:
        new_gens = mutate(new_gens, mutation_rate=0.05)  # 5% для кожного гена

    return get_evaluated_candidate(new_gens, all_locations)



# === Головна функція ===

def solve_with_genetic(ad_locations: List[AdLocation], constraints: Dict, generations: int, patience=500):
    if len(ad_locations)<=20:
        patience = 100
    elif len(ad_locations)<=70:
        patience = 500
    elif len(ad_locations)>=70:
        patience = 1000
    locations_object = {
        'north-west': [], 'north-east': [], 'south-west': [], 'south-east': [],
    }
    for loc in ad_locations:
        locations_object[loc.location].append(loc)
    flat_locations = get_flattened_locations(locations_object)
    population = generate_initial_population(locations_object, constraints)
    size = len(population)
    best = population[0]
    best_coverage = best.total_coverage
    stagnation_counter = 0
    actual_generations = 0

    for gen in range(generations):
        candidate1 = population[0]
        candidate2 = random.choice(population[1:])
        new_candidate = genetic_crossing(candidate1, candidate2, flat_locations)

        if satisfies_constraints(new_candidate, constraints):
            for i in range(len(population)):
                if new_candidate.total_coverage > population[i].total_coverage:
                    population.insert(i, new_candidate)
                    break
            if len(population) > size:
                population.pop()

        current_best = population[0]
        if current_best.total_coverage > best_coverage:
            best = current_best
            best_coverage = current_best.total_coverage
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        actual_generations += 1
        if stagnation_counter >= patience:
            break

    return best, actual_generations

