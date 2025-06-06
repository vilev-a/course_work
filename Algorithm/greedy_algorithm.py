def solve_with_greedy(locations, constraints):
    sorted_locations = sorted(locations, key=lambda loc: loc.coverage / loc.price, reverse=True)

    selected = []
    total_price = 0
    total_coverage = 0
    region_prices = {
        'north-west': 0,
        'north-east': 0,
        'south-west': 0,
        'south-east': 0,
    }

    for loc in sorted_locations:
        region_key = f"max{loc.location.title().replace('-', '')}RegionPrice"
        if (total_price + loc.price <= constraints['maxTotalPrice'] and
            region_prices[loc.location] + loc.price <= constraints[region_key]):
            
            selected.append(loc)
            total_price += loc.price
            total_coverage += loc.coverage
            region_prices[loc.location] += loc.price



    return {
        "coverage": total_coverage,
        "price": total_price,
        "locations": selected
    }