REGIONS = {
    "E": "North America",
    "F": "France",
    "J": "Japan",
    "K": "South Korea",
    "P": "Europe",
    "S": "Spain",
}


def get_region(game_code: str):
    region_code = game_code[-1]
    try:
        return REGIONS[region_code]
    except KeyError:
        print(f"Warning: unknown region code: {region_code}")
        return region_code
