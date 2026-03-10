"""Seed data for drinks catalog - 80 drinks across categories."""

DRINKS_DATA = [
    # SPIRITS - Vodka
    {
        "name": "Vodka (80 proof)",
        "category": "spirit",
        "subcategory": "vodka",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 1, "bitter": 1, "sour": 1, "savory": 1, "fruity": 1},
        "description": "Neutral grain spirit, clean and smooth",
        "base_spirit": None,
        "ingredients": ["Vodka"],
        "image_url": None
    },
    {
        "name": "Grey Goose Vodka",
        "category": "spirit",
        "subcategory": "vodka",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 1, "bitter": 1, "sour": 1, "savory": 2, "fruity": 1},
        "description": "Premium French vodka, ultra-smooth with subtle wheat notes",
        "base_spirit": None,
        "ingredients": ["Premium wheat vodka"],
        "image_url": None
    },

    # SPIRITS - Gin
    {
        "name": "London Dry Gin",
        "category": "spirit",
        "subcategory": "gin",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 1, "bitter": 3, "sour": 2, "savory": 2, "fruity": 2},
        "description": "Juniper-forward spirit with botanical notes",
        "base_spirit": None,
        "ingredients": ["Gin", "Juniper", "Botanicals"],
        "image_url": None
    },
    {
        "name": "Hendrick's Gin",
        "category": "spirit",
        "subcategory": "gin",
        "alcohol_content": 41.4,
        "flavor_profile": {"sweet": 2, "bitter": 2, "sour": 1, "savory": 3, "fruity": 3},
        "description": "Scottish gin infused with cucumber and rose",
        "base_spirit": None,
        "ingredients": ["Gin", "Cucumber", "Rose petals"],
        "image_url": None
    },

    # SPIRITS - Whiskey
    {
        "name": "Bourbon Whiskey",
        "category": "spirit",
        "subcategory": "bourbon",
        "alcohol_content": 43.0,
        "flavor_profile": {"sweet": 4, "bitter": 2, "sour": 1, "savory": 3, "fruity": 2},
        "description": "American whiskey with vanilla and caramel notes",
        "base_spirit": None,
        "ingredients": ["Bourbon"],
        "image_url": None
    },
    {
        "name": "Scotch Whisky",
        "category": "spirit",
        "subcategory": "scotch",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 2, "bitter": 3, "sour": 1, "savory": 4, "fruity": 1},
        "description": "Smoky Scottish whisky with peaty undertones",
        "base_spirit": None,
        "ingredients": ["Scotch"],
        "image_url": None
    },
    {
        "name": "Rye Whiskey",
        "category": "spirit",
        "subcategory": "rye",
        "alcohol_content": 45.0,
        "flavor_profile": {"sweet": 2, "bitter": 4, "sour": 1, "savory": 4, "fruity": 1},
        "description": "Spicy American whiskey with bold character",
        "base_spirit": None,
        "ingredients": ["Rye whiskey"],
        "image_url": None
    },
    {
        "name": "Irish Whiskey",
        "category": "spirit",
        "subcategory": "irish_whiskey",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 1, "savory": 2, "fruity": 2},
        "description": "Smooth triple-distilled Irish whiskey",
        "base_spirit": None,
        "ingredients": ["Irish whiskey"],
        "image_url": None
    },

    # SPIRITS - Rum
    {
        "name": "White Rum",
        "category": "spirit",
        "subcategory": "rum",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 3, "bitter": 1, "sour": 1, "savory": 1, "fruity": 2},
        "description": "Light-bodied rum, ideal for cocktails",
        "base_spirit": None,
        "ingredients": ["White rum"],
        "image_url": None
    },
    {
        "name": "Dark Rum",
        "category": "spirit",
        "subcategory": "rum",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 4, "bitter": 2, "sour": 1, "savory": 3, "fruity": 3},
        "description": "Rich aged rum with molasses and spice",
        "base_spirit": None,
        "ingredients": ["Dark rum"],
        "image_url": None
    },
    {
        "name": "Spiced Rum",
        "category": "spirit",
        "subcategory": "rum",
        "alcohol_content": 35.0,
        "flavor_profile": {"sweet": 4, "bitter": 1, "sour": 1, "savory": 4, "fruity": 2},
        "description": "Rum infused with vanilla, cinnamon, and warm spices",
        "base_spirit": None,
        "ingredients": ["Rum", "Spices", "Vanilla"],
        "image_url": None
    },

    # SPIRITS - Tequila/Mezcal
    {
        "name": "Blanco Tequila",
        "category": "spirit",
        "subcategory": "tequila",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 2, "bitter": 2, "sour": 2, "savory": 3, "fruity": 2},
        "description": "Unaged agave spirit with bright, crisp flavor",
        "base_spirit": None,
        "ingredients": ["Tequila"],
        "image_url": None
    },
    {
        "name": "Reposado Tequila",
        "category": "spirit",
        "subcategory": "tequila",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 1, "savory": 3, "fruity": 2},
        "description": "Aged tequila with oak and vanilla notes",
        "base_spirit": None,
        "ingredients": ["Aged tequila"],
        "image_url": None
    },
    {
        "name": "Mezcal",
        "category": "spirit",
        "subcategory": "mezcal",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 1, "bitter": 3, "sour": 2, "savory": 5, "fruity": 1},
        "description": "Smoky agave spirit with complex earthy flavors",
        "base_spirit": None,
        "ingredients": ["Mezcal"],
        "image_url": None
    },

    # COCKTAILS - Classic
    {
        "name": "Martini",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 30.0,
        "flavor_profile": {"sweet": 1, "bitter": 3, "sour": 1, "savory": 3, "fruity": 2},
        "description": "Classic gin cocktail with dry vermouth",
        "base_spirit": "gin",
        "ingredients": ["Gin", "Dry vermouth", "Olive or lemon twist"],
        "image_url": None
    },
    {
        "name": "Manhattan",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 28.0,
        "flavor_profile": {"sweet": 3, "bitter": 3, "sour": 1, "savory": 3, "fruity": 2},
        "description": "Whiskey cocktail with sweet vermouth and bitters",
        "base_spirit": "whiskey",
        "ingredients": ["Rye whiskey", "Sweet vermouth", "Angostura bitters", "Cherry"],
        "image_url": None
    },
    {
        "name": "Old Fashioned",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 32.0,
        "flavor_profile": {"sweet": 4, "bitter": 3, "sour": 1, "savory": 3, "fruity": 2},
        "description": "Timeless whiskey cocktail with sugar and bitters",
        "base_spirit": "bourbon",
        "ingredients": ["Bourbon", "Sugar", "Angostura bitters", "Orange peel"],
        "image_url": None
    },
    {
        "name": "Negroni",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 24.0,
        "flavor_profile": {"sweet": 2, "bitter": 5, "sour": 1, "savory": 2, "fruity": 3},
        "description": "Equal parts gin, Campari, and sweet vermouth",
        "base_spirit": "gin",
        "ingredients": ["Gin", "Campari", "Sweet vermouth", "Orange peel"],
        "image_url": None
    },
    {
        "name": "Margarita",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 18.0,
        "flavor_profile": {"sweet": 3, "bitter": 1, "sour": 5, "savory": 2, "fruity": 4},
        "description": "Tequila cocktail with lime and orange liqueur",
        "base_spirit": "tequila",
        "ingredients": ["Tequila", "Lime juice", "Cointreau", "Salt"],
        "image_url": None
    },
    {
        "name": "Mojito",
        "category": "cocktail",
        "subcategory": "refreshing",
        "alcohol_content": 10.0,
        "flavor_profile": {"sweet": 4, "bitter": 1, "sour": 4, "savory": 1, "fruity": 3},
        "description": "Cuban rum cocktail with mint and lime",
        "base_spirit": "rum",
        "ingredients": ["White rum", "Lime juice", "Mint", "Sugar", "Soda water"],
        "image_url": None
    },
    {
        "name": "Daiquiri",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 20.0,
        "flavor_profile": {"sweet": 3, "bitter": 1, "sour": 5, "savory": 1, "fruity": 3},
        "description": "Simple rum cocktail with lime and sugar",
        "base_spirit": "rum",
        "ingredients": ["White rum", "Lime juice", "Simple syrup"],
        "image_url": None
    },
    {
        "name": "Whiskey Sour",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 20.0,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 5, "savory": 2, "fruity": 2},
        "description": "Bourbon shaken with lemon and egg white",
        "base_spirit": "bourbon",
        "ingredients": ["Bourbon", "Lemon juice", "Simple syrup", "Egg white", "Cherry"],
        "image_url": None
    },
    {
        "name": "Mai Tai",
        "category": "cocktail",
        "subcategory": "tropical",
        "alcohol_content": 22.0,
        "flavor_profile": {"sweet": 4, "bitter": 2, "sour": 4, "savory": 1, "fruity": 5},
        "description": "Tiki rum cocktail with orgeat and lime",
        "base_spirit": "rum",
        "ingredients": ["Dark rum", "White rum", "Lime juice", "Orgeat", "Orange liqueur"],
        "image_url": None
    },
    {
        "name": "Cosmopolitan",
        "category": "cocktail",
        "subcategory": "modern",
        "alcohol_content": 18.0,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 4, "savory": 1, "fruity": 5},
        "description": "Vodka cocktail with cranberry and lime",
        "base_spirit": "vodka",
        "ingredients": ["Vodka", "Cointreau", "Cranberry juice", "Lime juice"],
        "image_url": None
    },

    # COCKTAILS - Modern/Popular
    {
        "name": "Espresso Martini",
        "category": "cocktail",
        "subcategory": "modern",
        "alcohol_content": 20.0,
        "flavor_profile": {"sweet": 4, "bitter": 4, "sour": 1, "savory": 2, "fruity": 1},
        "description": "Vodka shaken with espresso and coffee liqueur",
        "base_spirit": "vodka",
        "ingredients": ["Vodka", "Espresso", "Kahlúa", "Simple syrup"],
        "image_url": None
    },
    {
        "name": "Aperol Spritz",
        "category": "cocktail",
        "subcategory": "refreshing",
        "alcohol_content": 8.0,
        "flavor_profile": {"sweet": 3, "bitter": 3, "sour": 2, "savory": 1, "fruity": 4},
        "description": "Italian spritz with Aperol and prosecco",
        "base_spirit": "aperol",
        "ingredients": ["Aperol", "Prosecco", "Soda water", "Orange slice"],
        "image_url": None
    },
    {
        "name": "Moscow Mule",
        "category": "cocktail",
        "subcategory": "refreshing",
        "alcohol_content": 12.0,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 3, "savory": 2, "fruity": 2},
        "description": "Vodka with ginger beer and lime",
        "base_spirit": "vodka",
        "ingredients": ["Vodka", "Ginger beer", "Lime juice"],
        "image_url": None
    },
    {
        "name": "Paloma",
        "category": "cocktail",
        "subcategory": "refreshing",
        "alcohol_content": 12.0,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 4, "savory": 2, "fruity": 4},
        "description": "Tequila highball with grapefruit and soda",
        "base_spirit": "tequila",
        "ingredients": ["Tequila", "Grapefruit soda", "Lime juice", "Salt"],
        "image_url": None
    },
    {
        "name": "French 75",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 15.0,
        "flavor_profile": {"sweet": 3, "bitter": 1, "sour": 4, "savory": 1, "fruity": 3},
        "description": "Gin cocktail topped with champagne",
        "base_spirit": "gin",
        "ingredients": ["Gin", "Lemon juice", "Simple syrup", "Champagne"],
        "image_url": None
    },
    {
        "name": "Pisco Sour",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 18.0,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 5, "savory": 1, "fruity": 3},
        "description": "Peruvian brandy cocktail with lime and egg white",
        "base_spirit": "pisco",
        "ingredients": ["Pisco", "Lime juice", "Simple syrup", "Egg white", "Bitters"],
        "image_url": None
    },
    {
        "name": "Dark 'n' Stormy",
        "category": "cocktail",
        "subcategory": "refreshing",
        "alcohol_content": 14.0,
        "flavor_profile": {"sweet": 4, "bitter": 2, "sour": 3, "savory": 3, "fruity": 2},
        "description": "Dark rum with ginger beer and lime",
        "base_spirit": "rum",
        "ingredients": ["Dark rum", "Ginger beer", "Lime juice"],
        "image_url": None
    },
    {
        "name": "Sazerac",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 35.0,
        "flavor_profile": {"sweet": 2, "bitter": 4, "sour": 1, "savory": 4, "fruity": 1},
        "description": "New Orleans rye cocktail with absinthe rinse",
        "base_spirit": "rye",
        "ingredients": ["Rye whiskey", "Sugar", "Peychaud's bitters", "Absinthe", "Lemon peel"],
        "image_url": None
    },
    {
        "name": "Bloody Mary",
        "category": "cocktail",
        "subcategory": "savory",
        "alcohol_content": 12.0,
        "flavor_profile": {"sweet": 2, "bitter": 2, "sour": 3, "savory": 5, "fruity": 2},
        "description": "Savory vodka cocktail with tomato juice and spices",
        "base_spirit": "vodka",
        "ingredients": ["Vodka", "Tomato juice", "Lemon juice", "Worcestershire", "Hot sauce", "Celery"],
        "image_url": None
    },
    {
        "name": "Piña Colada",
        "category": "cocktail",
        "subcategory": "tropical",
        "alcohol_content": 13.0,
        "flavor_profile": {"sweet": 5, "bitter": 1, "sour": 2, "savory": 1, "fruity": 5},
        "description": "Tropical rum cocktail with pineapple and coconut",
        "base_spirit": "rum",
        "ingredients": ["White rum", "Pineapple juice", "Coconut cream"],
        "image_url": None
    },

    # WINE - Red
    {
        "name": "Cabernet Sauvignon",
        "category": "wine",
        "subcategory": "red_wine",
        "alcohol_content": 13.5,
        "flavor_profile": {"sweet": 2, "bitter": 3, "sour": 2, "savory": 4, "fruity": 4},
        "description": "Full-bodied red wine with blackcurrant and oak",
        "base_spirit": None,
        "ingredients": ["Cabernet Sauvignon grapes"],
        "image_url": None
    },
    {
        "name": "Merlot",
        "category": "wine",
        "subcategory": "red_wine",
        "alcohol_content": 13.5,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 2, "savory": 3, "fruity": 4},
        "description": "Medium-bodied red wine with plum and chocolate",
        "base_spirit": None,
        "ingredients": ["Merlot grapes"],
        "image_url": None
    },
    {
        "name": "Pinot Noir",
        "category": "wine",
        "subcategory": "red_wine",
        "alcohol_content": 13.0,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 3, "savory": 3, "fruity": 4},
        "description": "Light-bodied red wine with cherry and earth",
        "base_spirit": None,
        "ingredients": ["Pinot Noir grapes"],
        "image_url": None
    },
    {
        "name": "Malbec",
        "category": "wine",
        "subcategory": "red_wine",
        "alcohol_content": 14.0,
        "flavor_profile": {"sweet": 3, "bitter": 3, "sour": 2, "savory": 4, "fruity": 4},
        "description": "Bold Argentinian red wine with blackberry and smoke",
        "base_spirit": None,
        "ingredients": ["Malbec grapes"],
        "image_url": None
    },
    {
        "name": "Chianti",
        "category": "wine",
        "subcategory": "red_wine",
        "alcohol_content": 12.5,
        "flavor_profile": {"sweet": 2, "bitter": 3, "sour": 4, "savory": 4, "fruity": 3},
        "description": "Italian red wine with cherry and herbs",
        "base_spirit": None,
        "ingredients": ["Sangiovese grapes"],
        "image_url": None
    },

    # WINE - White
    {
        "name": "Chardonnay",
        "category": "wine",
        "subcategory": "white_wine",
        "alcohol_content": 13.0,
        "flavor_profile": {"sweet": 3, "bitter": 1, "sour": 3, "savory": 2, "fruity": 4},
        "description": "Full-bodied white wine with butter and vanilla",
        "base_spirit": None,
        "ingredients": ["Chardonnay grapes"],
        "image_url": None
    },
    {
        "name": "Sauvignon Blanc",
        "category": "wine",
        "subcategory": "white_wine",
        "alcohol_content": 12.5,
        "flavor_profile": {"sweet": 2, "bitter": 2, "sour": 4, "savory": 3, "fruity": 4},
        "description": "Crisp white wine with citrus and grass",
        "base_spirit": None,
        "ingredients": ["Sauvignon Blanc grapes"],
        "image_url": None
    },
    {
        "name": "Pinot Grigio",
        "category": "wine",
        "subcategory": "white_wine",
        "alcohol_content": 12.0,
        "flavor_profile": {"sweet": 2, "bitter": 1, "sour": 4, "savory": 2, "fruity": 3},
        "description": "Light Italian white wine with pear and apple",
        "base_spirit": None,
        "ingredients": ["Pinot Grigio grapes"],
        "image_url": None
    },
    {
        "name": "Riesling",
        "category": "wine",
        "subcategory": "white_wine",
        "alcohol_content": 11.0,
        "flavor_profile": {"sweet": 4, "bitter": 1, "sour": 4, "savory": 1, "fruity": 5},
        "description": "Aromatic white wine with peach and honey",
        "base_spirit": None,
        "ingredients": ["Riesling grapes"],
        "image_url": None
    },

    # WINE - Sparkling
    {
        "name": "Champagne",
        "category": "wine",
        "subcategory": "sparkling",
        "alcohol_content": 12.0,
        "flavor_profile": {"sweet": 2, "bitter": 2, "sour": 3, "savory": 2, "fruity": 3},
        "description": "French sparkling wine with toast and citrus",
        "base_spirit": None,
        "ingredients": ["Champagne grapes"],
        "image_url": None
    },
    {
        "name": "Prosecco",
        "category": "wine",
        "subcategory": "sparkling",
        "alcohol_content": 11.0,
        "flavor_profile": {"sweet": 3, "bitter": 1, "sour": 3, "savory": 1, "fruity": 4},
        "description": "Italian sparkling wine with pear and flowers",
        "base_spirit": None,
        "ingredients": ["Prosecco grapes"],
        "image_url": None
    },
    {
        "name": "Cava",
        "category": "wine",
        "subcategory": "sparkling",
        "alcohol_content": 11.5,
        "flavor_profile": {"sweet": 2, "bitter": 2, "sour": 3, "savory": 2, "fruity": 3},
        "description": "Spanish sparkling wine, crisp and refreshing",
        "base_spirit": None,
        "ingredients": ["Cava grapes"],
        "image_url": None
    },

    # BEER - IPA
    {
        "name": "IPA (India Pale Ale)",
        "category": "beer",
        "subcategory": "ipa",
        "alcohol_content": 6.5,
        "flavor_profile": {"sweet": 2, "bitter": 5, "sour": 1, "savory": 2, "fruity": 4},
        "description": "Hoppy American beer with citrus and pine",
        "base_spirit": None,
        "ingredients": ["Hops", "Malt", "Yeast", "Water"],
        "image_url": None
    },
    {
        "name": "Hazy IPA",
        "category": "beer",
        "subcategory": "ipa",
        "alcohol_content": 6.8,
        "flavor_profile": {"sweet": 3, "bitter": 4, "sour": 1, "savory": 2, "fruity": 5},
        "description": "Unfiltered IPA with juicy tropical fruit flavors",
        "base_spirit": None,
        "ingredients": ["Hops", "Malt", "Yeast", "Water"],
        "image_url": None
    },
    {
        "name": "Double IPA",
        "category": "beer",
        "subcategory": "ipa",
        "alcohol_content": 8.5,
        "flavor_profile": {"sweet": 3, "bitter": 5, "sour": 1, "savory": 3, "fruity": 4},
        "description": "High-alcohol IPA with intense hop character",
        "base_spirit": None,
        "ingredients": ["Extra hops", "Malt", "Yeast", "Water"],
        "image_url": None
    },

    # BEER - Pale Ale
    {
        "name": "Pale Ale",
        "category": "beer",
        "subcategory": "pale_ale",
        "alcohol_content": 5.5,
        "flavor_profile": {"sweet": 3, "bitter": 3, "sour": 1, "savory": 2, "fruity": 3},
        "description": "Balanced beer with malt and hop flavor",
        "base_spirit": None,
        "ingredients": ["Hops", "Malt", "Yeast", "Water"],
        "image_url": None
    },

    # BEER - Lager
    {
        "name": "Pilsner",
        "category": "beer",
        "subcategory": "lager",
        "alcohol_content": 5.0,
        "flavor_profile": {"sweet": 2, "bitter": 3, "sour": 1, "savory": 2, "fruity": 1},
        "description": "Crisp Czech lager with noble hops",
        "base_spirit": None,
        "ingredients": ["Pilsner malt", "Hops", "Yeast", "Water"],
        "image_url": None
    },
    {
        "name": "Lager",
        "category": "beer",
        "subcategory": "lager",
        "alcohol_content": 4.5,
        "flavor_profile": {"sweet": 2, "bitter": 2, "sour": 1, "savory": 2, "fruity": 1},
        "description": "Clean, crisp, easy-drinking beer",
        "base_spirit": None,
        "ingredients": ["Malt", "Hops", "Yeast", "Water"],
        "image_url": None
    },
    {
        "name": "Helles Lager",
        "category": "beer",
        "subcategory": "lager",
        "alcohol_content": 5.2,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 1, "savory": 2, "fruity": 1},
        "description": "Bavarian lager with soft malt character",
        "base_spirit": None,
        "ingredients": ["Pilsner malt", "Noble hops", "Yeast", "Water"],
        "image_url": None
    },

    # BEER - Stout/Porter
    {
        "name": "Stout",
        "category": "beer",
        "subcategory": "stout",
        "alcohol_content": 5.5,
        "flavor_profile": {"sweet": 3, "bitter": 4, "sour": 1, "savory": 4, "fruity": 2},
        "description": "Dark beer with coffee and chocolate notes",
        "base_spirit": None,
        "ingredients": ["Roasted malt", "Hops", "Yeast", "Water"],
        "image_url": None
    },
    {
        "name": "Guinness (Dry Stout)",
        "category": "beer",
        "subcategory": "stout",
        "alcohol_content": 4.2,
        "flavor_profile": {"sweet": 2, "bitter": 4, "sour": 1, "savory": 5, "fruity": 1},
        "description": "Iconic Irish dry stout with roasted barley",
        "base_spirit": None,
        "ingredients": ["Roasted barley", "Hops", "Yeast", "Water"],
        "image_url": None
    },
    {
        "name": "Imperial Stout",
        "category": "beer",
        "subcategory": "stout",
        "alcohol_content": 9.0,
        "flavor_profile": {"sweet": 4, "bitter": 4, "sour": 1, "savory": 5, "fruity": 2},
        "description": "High-alcohol stout with intense flavors",
        "base_spirit": None,
        "ingredients": ["Roasted malt", "Hops", "Yeast", "Water"],
        "image_url": None
    },
    {
        "name": "Porter",
        "category": "beer",
        "subcategory": "porter",
        "alcohol_content": 5.0,
        "flavor_profile": {"sweet": 3, "bitter": 3, "sour": 1, "savory": 4, "fruity": 2},
        "description": "Dark beer with chocolate and toffee",
        "base_spirit": None,
        "ingredients": ["Chocolate malt", "Hops", "Yeast", "Water"],
        "image_url": None
    },

    # BEER - Wheat Beer
    {
        "name": "Hefeweizen",
        "category": "beer",
        "subcategory": "wheat",
        "alcohol_content": 5.4,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 2, "savory": 1, "fruity": 4},
        "description": "German wheat beer with banana and clove",
        "base_spirit": None,
        "ingredients": ["Wheat", "Barley", "Yeast", "Water"],
        "image_url": None
    },
    {
        "name": "Witbier",
        "category": "beer",
        "subcategory": "wheat",
        "alcohol_content": 4.5,
        "flavor_profile": {"sweet": 3, "bitter": 1, "sour": 3, "savory": 1, "fruity": 4},
        "description": "Belgian wheat beer with orange and coriander",
        "base_spirit": None,
        "ingredients": ["Wheat", "Orange peel", "Coriander", "Yeast"],
        "image_url": None
    },

    # BEER - Sour
    {
        "name": "Berliner Weisse",
        "category": "beer",
        "subcategory": "sour",
        "alcohol_content": 3.5,
        "flavor_profile": {"sweet": 2, "bitter": 1, "sour": 5, "savory": 1, "fruity": 3},
        "description": "Tart German wheat beer, low alcohol",
        "base_spirit": None,
        "ingredients": ["Wheat", "Lactobacillus", "Yeast"],
        "image_url": None
    },
    {
        "name": "Gose",
        "category": "beer",
        "subcategory": "sour",
        "alcohol_content": 4.2,
        "flavor_profile": {"sweet": 2, "bitter": 1, "sour": 4, "savory": 3, "fruity": 3},
        "description": "Salty, sour German wheat beer with coriander",
        "base_spirit": None,
        "ingredients": ["Wheat", "Salt", "Coriander", "Lactobacillus"],
        "image_url": None
    },

    # LIQUEURS
    {
        "name": "Amaretto",
        "category": "liqueur",
        "subcategory": "nut",
        "alcohol_content": 28.0,
        "flavor_profile": {"sweet": 5, "bitter": 2, "sour": 1, "savory": 2, "fruity": 2},
        "description": "Sweet Italian almond liqueur",
        "base_spirit": None,
        "ingredients": ["Almonds", "Apricot pits", "Sugar"],
        "image_url": None
    },
    {
        "name": "Baileys Irish Cream",
        "category": "liqueur",
        "subcategory": "cream",
        "alcohol_content": 17.0,
        "flavor_profile": {"sweet": 5, "bitter": 1, "sour": 1, "savory": 3, "fruity": 1},
        "description": "Creamy Irish whiskey liqueur",
        "base_spirit": "whiskey",
        "ingredients": ["Irish whiskey", "Cream", "Cocoa"],
        "image_url": None
    },
    {
        "name": "Cointreau",
        "category": "liqueur",
        "subcategory": "orange",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 4, "bitter": 2, "sour": 2, "savory": 1, "fruity": 5},
        "description": "Premium triple sec orange liqueur",
        "base_spirit": None,
        "ingredients": ["Sweet and bitter orange peels", "Sugar"],
        "image_url": None
    },
    {
        "name": "Kahlúa",
        "category": "liqueur",
        "subcategory": "coffee",
        "alcohol_content": 20.0,
        "flavor_profile": {"sweet": 5, "bitter": 3, "sour": 1, "savory": 2, "fruity": 1},
        "description": "Mexican coffee liqueur",
        "base_spirit": "rum",
        "ingredients": ["Coffee", "Rum", "Vanilla", "Sugar"],
        "image_url": None
    },
    {
        "name": "Chambord",
        "category": "liqueur",
        "subcategory": "fruit",
        "alcohol_content": 16.5,
        "flavor_profile": {"sweet": 5, "bitter": 1, "sour": 2, "savory": 1, "fruity": 5},
        "description": "French black raspberry liqueur",
        "base_spirit": None,
        "ingredients": ["Raspberries", "Blackberries", "Vanilla", "Honey"],
        "image_url": None
    },
    {
        "name": "Grand Marnier",
        "category": "liqueur",
        "subcategory": "orange",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 4, "bitter": 2, "sour": 2, "savory": 3, "fruity": 5},
        "description": "Cognac-based orange liqueur",
        "base_spirit": "cognac",
        "ingredients": ["Cognac", "Bitter orange", "Sugar"],
        "image_url": None
    },
    {
        "name": "St-Germain",
        "category": "liqueur",
        "subcategory": "floral",
        "alcohol_content": 20.0,
        "flavor_profile": {"sweet": 4, "bitter": 1, "sour": 2, "savory": 1, "fruity": 5},
        "description": "French elderflower liqueur",
        "base_spirit": None,
        "ingredients": ["Elderflowers", "Sugar"],
        "image_url": None
    },
    {
        "name": "Campari",
        "category": "liqueur",
        "subcategory": "bitter",
        "alcohol_content": 25.0,
        "flavor_profile": {"sweet": 3, "bitter": 5, "sour": 2, "savory": 2, "fruity": 3},
        "description": "Italian bitter aperitif with herbs",
        "base_spirit": None,
        "ingredients": ["Herbs", "Fruit", "Spices"],
        "image_url": None
    },
    {
        "name": "Aperol",
        "category": "liqueur",
        "subcategory": "bitter",
        "alcohol_content": 11.0,
        "flavor_profile": {"sweet": 4, "bitter": 3, "sour": 2, "savory": 1, "fruity": 4},
        "description": "Italian orange aperitif, lighter than Campari",
        "base_spirit": None,
        "ingredients": ["Bitter orange", "Rhubarb", "Herbs"],
        "image_url": None
    },
    {
        "name": "Frangelico",
        "category": "liqueur",
        "subcategory": "nut",
        "alcohol_content": 20.0,
        "flavor_profile": {"sweet": 5, "bitter": 1, "sour": 1, "savory": 3, "fruity": 1},
        "description": "Italian hazelnut liqueur",
        "base_spirit": None,
        "ingredients": ["Hazelnuts", "Vanilla", "Cocoa"],
        "image_url": None
    },

    # ADDITIONAL COCKTAILS
    {
        "name": "Tom Collins",
        "category": "cocktail",
        "subcategory": "refreshing",
        "alcohol_content": 10.0,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 4, "savory": 1, "fruity": 3},
        "description": "Gin highball with lemon and soda",
        "base_spirit": "gin",
        "ingredients": ["Gin", "Lemon juice", "Simple syrup", "Soda water"],
        "image_url": None
    },
    {
        "name": "Gimlet",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 25.0,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 5, "savory": 2, "fruity": 2},
        "description": "Simple gin and lime cocktail",
        "base_spirit": "gin",
        "ingredients": ["Gin", "Lime juice", "Simple syrup"],
        "image_url": None
    },
    {
        "name": "Boulevardier",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 30.0,
        "flavor_profile": {"sweet": 3, "bitter": 5, "sour": 1, "savory": 3, "fruity": 2},
        "description": "Whiskey Negroni with bourbon instead of gin",
        "base_spirit": "bourbon",
        "ingredients": ["Bourbon", "Campari", "Sweet vermouth"],
        "image_url": None
    },
    {
        "name": "Aviation",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 22.0,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 4, "savory": 1, "fruity": 4},
        "description": "Floral gin cocktail with crème de violette",
        "base_spirit": "gin",
        "ingredients": ["Gin", "Lemon juice", "Maraschino liqueur", "Crème de violette"],
        "image_url": None
    },
    {
        "name": "Mint Julep",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 30.0,
        "flavor_profile": {"sweet": 4, "bitter": 2, "sour": 1, "savory": 2, "fruity": 2},
        "description": "Kentucky Derby bourbon cocktail with mint",
        "base_spirit": "bourbon",
        "ingredients": ["Bourbon", "Mint", "Sugar", "Crushed ice"],
        "image_url": None
    },
    {
        "name": "Caipirinha",
        "category": "cocktail",
        "subcategory": "classic",
        "alcohol_content": 25.0,
        "flavor_profile": {"sweet": 4, "bitter": 1, "sour": 5, "savory": 1, "fruity": 4},
        "description": "Brazilian cachaça cocktail with lime and sugar",
        "base_spirit": "cachaça",
        "ingredients": ["Cachaça", "Lime", "Sugar"],
        "image_url": None
    },

    # SPIRITS - Cognac & Brandy
    {
        "name": "Cognac",
        "category": "spirit",
        "subcategory": "cognac",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 4, "bitter": 2, "sour": 1, "savory": 3, "fruity": 4},
        "description": "French grape brandy from the Cognac region, smooth and complex",
        "base_spirit": None,
        "ingredients": ["Cognac"],
        "image_url": None
    },
    {
        "name": "Hennessy VS",
        "category": "spirit",
        "subcategory": "cognac",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 4, "bitter": 2, "sour": 1, "savory": 3, "fruity": 4},
        "description": "Premium cognac with oak and fruit notes",
        "base_spirit": None,
        "ingredients": ["Cognac"],
        "image_url": None
    },
    {
        "name": "Brandy",
        "category": "spirit",
        "subcategory": "brandy",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 4, "bitter": 2, "sour": 1, "savory": 2, "fruity": 4},
        "description": "Distilled wine spirit, rich and warming",
        "base_spirit": None,
        "ingredients": ["Brandy"],
        "image_url": None
    },
    {
        "name": "Armagnac",
        "category": "spirit",
        "subcategory": "brandy",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 3, "bitter": 2, "sour": 1, "savory": 3, "fruity": 4},
        "description": "French brandy from Gascony, rustic and bold",
        "base_spirit": None,
        "ingredients": ["Armagnac"],
        "image_url": None
    },
    {
        "name": "Calvados",
        "category": "spirit",
        "subcategory": "brandy",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 4, "bitter": 1, "sour": 2, "savory": 2, "fruity": 5},
        "description": "Apple brandy from Normandy, France",
        "base_spirit": None,
        "ingredients": ["Apple brandy"],
        "image_url": None
    },

    # SPIRITS - Mezcal & Pisco
    {
        "name": "Mezcal",
        "category": "spirit",
        "subcategory": "mezcal",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 2, "bitter": 3, "sour": 1, "savory": 4, "fruity": 2},
        "description": "Smoky Mexican agave spirit",
        "base_spirit": None,
        "ingredients": ["Mezcal"],
        "image_url": None
    },
    {
        "name": "Pisco",
        "category": "spirit",
        "subcategory": "pisco",
        "alcohol_content": 40.0,
        "flavor_profile": {"sweet": 3, "bitter": 1, "sour": 1, "savory": 2, "fruity": 4},
        "description": "South American grape brandy, clear and aromatic",
        "base_spirit": None,
        "ingredients": ["Pisco"],
        "image_url": None
    },

    # SPIRITS - Sake
    {
        "name": "Sake",
        "category": "spirit",
        "subcategory": "sake",
        "alcohol_content": 15.0,
        "flavor_profile": {"sweet": 3, "bitter": 1, "sour": 2, "savory": 3, "fruity": 2},
        "description": "Japanese rice wine, delicate and smooth",
        "base_spirit": None,
        "ingredients": ["Rice wine"],
        "image_url": None
    },
]
