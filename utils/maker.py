MAKERS = {
    "JF": "ARC SYSTEM WORKS",
    "XS": "Aksys Games",
}


def get_maker(maker_code: str):
    try:
        return MAKERS[maker_code]
    except KeyError:
        print(f"Warning: unknown maker: {maker_code}")
        return maker_code
