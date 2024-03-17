from search.search import Search
import time
import pandas as pd

with Search() as bot:
    bot.land_first_page()
    bot.product_search('Samsung Galaxy S10')
    bot.apply_filters(category="Mobiles", brand="SAMSUNG", flipkart_assured="Plus (FAssured)", price="Price -- High to Low")
    data = bot.get_parameters()
    