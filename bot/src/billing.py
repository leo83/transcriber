    
class Pricing:

    __BASE_PRICE_10 = 199

    pricing_detail = {
        10: __BASE_PRICE_10, 
        20: round(__BASE_PRICE_10 * 2  * .98 / 100) * 100 -1,
        50:  round(__BASE_PRICE_10 * 5 * 0.95 / 100) * 100 -1,
        'Unlim': round(__BASE_PRICE_10 * 10 * 0.85 / 100) * 100 -1
    }
