import pandas as pd
import math

class Ingredient:

    def __init__(self, csv_path, ingredient_name):

        data = pd.read_csv(csv_path)

        database_names = (
            data["Description"]
            .str.strip()
            .str.casefold()
        )

        search_name = (
            ingredient_name
            .strip()
            .casefold()
        )

        result = data[
            database_names == search_name
        ]

        if result.empty:
            raise ValueError(
                f'Zutat "{ingredient_name}" '
                f'nicht in Datenbank'
            )

        row = result.iloc[0]

        self.name = row["Description"]
        self.category = row["Category"]
        self.carbohydrates = row["Data.Carbohydrate"]
        self.protein = row["Data.Protein"]
        self.fat = row["Data.Fat.Total Lipid"]
        self.fiber = row["Data.Fiber"]
        self.sugar = row["Data.Sugar Total"]

    def estimate_calories(self):

        digestible_carbs = max(
            0,
            self.carbohydrates - self.fiber
        )

        return (
            digestible_carbs * 4
            + self.fiber * 2
            + self.protein * 4
            + self.fat * 9
        )

    def show_info(self):
        print(f"Name: {self.name}")
        print(f"Kategorie: {self.category}")
        print(f"Protein: {self.protein} g")
        print(f"Kohlenhydrate: {self.carbohydrates} g")
        print(f"Ballaststoffe: {self.fiber} g")
        print(f"Fett: {self.fat} g")

class Serving:
    def __init__(self, s_path, i_path, serving_name):

        servings_data = pd.read_csv(s_path)
        servings = servings_data.values.tolist()

        for obj in servings:
            if obj[0] == serving_name:
                serving = obj[1:]

        ingredient_list = {}

        for i in range(0,len(serving),2):
            if type(serving[i]) == str:
                ingredient_name = serving[i]

                ingredient_list[ingredient_name] = serving[i + 1]

        self.carbs = 0
        self.protein = 0
        self.fat = 0
        self.fiber = 0
        self.sugar = 0
        self.calories = 0

        for ingredient in ingredient_list:
            ingredientstats = Ingredient(i_path, ingredient)
            self.carbs += ingredientstats.carbohydrates * ingredient_list[ingredient]
            self.protein += ingredientstats.protein * ingredient_list[ingredient]
            self.fat += ingredientstats.fat * ingredient_list[ingredient]
            self.fiber += ingredientstats.fiber * ingredient_list[ingredient]
            self.sugar += ingredientstats.sugar * ingredient_list[ingredient]
            self.calories += ingredientstats.estimate_calories() * ingredient_list[ingredient]

class Meal:
    def __init__(self, serving_1, serving_2, gram_1, gram_2,):
        self.serving_1 = serving_1
        self.serving_2 = serving_2
        self.gram_1 = gram_1
        self.gram_2 = gram_2

    def read_cookingtime(self):
        self.cooking_time1 = self.serving_1.cooking_time
        self.cooking_time2 = self.serving_2.cooking_time

        return self.cooking_time1, self.cooking_time2
            
    def read_protein(self):
        self.protein1 = self.serving_1.protein
        self.protein2 = self.serving_2.protein

        return self.protein1, self.protein2

    def read_fat(self):
        self.fat1 = self.serving_1.fat
        self.fat2 = self.serving_2.fat

        return self.fat1, self.fat2

    def read_carbohydrates(self):
        self.carbohydrates1 = self.serving_1.carbohydrates
        self.carbohydrates2 = self.serving_2.carbohydrates

        return self.carbohydrates1, self.carbohydrates2

    def read_fiber(self):
        self.fiber1 = self.serving_1.fiber
        self.fiber2 = self.serving_2.fiber

        return self.fiber1, self.fiber2

    def read_sugar(self):
        self.sugar1 = self.serving_1.sugar
        self.sugar2 = self.serving_2.sugar

        return self.sugar1, self.sugar2

    def read_calories(self):
        self.calories1 = self.serving_1.estimate_calories()
        self.calories2 = self.serving_2.estimate_calories()

        return self.calories1, self.calories2

    def read_utens(self):
        self.utens1 = self.serving_1.utens
        self.utens2 = self.serving_2.utens

        return self.utens1, self.utens2

    def calculate_total_protein(self):
        total_protein = (
            self.protein1 * self.gram_1 / 100 
            + self.protein2 * self.gram_2 / 100
        )
        return total_protein

    def calculate_total_fat(self):
        total_fat = (
            self.fat1 * self.gram_1 / 100 
            + self.fat2 * self.gram_2 / 100
        )
        return total_fat

    def calculate_total_carbohydrates(self):
        total_carbohydrates = (
            self.carbohydrates1 * self.gram_1 / 100 
            + self.carbohydrates2 * self.gram_2 / 100
        )
        return total_carbohydrates

    def calculate_total_fiber(self):
        total_fiber = (
            self.fiber1 * self.gram_1 / 100
            + self.fiber2 * self.gram_2 / 100
        )
        return total_fiber

    def calculate_total_sugar(self):
        total_sugar = (
            self.sugar1 * self.gram_1 / 100
            + self.sugar2 * self.gram_2 / 100
        )
        return total_sugar

    def calculate_total_calories(self):
        total_calories = (
            self.calories1 * self.gram_1 / 100
            + self.calories2 * self.gram_2 / 100
        )
        return total_calories

    def calculate_total_utens(self):
        total_utens = self.utens1 + self.utens2
        return total_utens

    def calculate_total_cooking_time(self):
        total_cooking_time = self.cooking_time1 + self.cooking_time2
        return total_cooking_time
    
    def show_meal_info(self):
        print(f"Gesamtprotein: {self.calculate_total_protein()} g")
        print(f"Gesamtfett: {self.calculate_total_fat()} g")
        print(f"Gesamtkohlenhydrate: {self.calculate_total_carbohydrates()} g")
        print(f"Gesamtballaststoffe: {self.calculate_total_fiber()} g")
        print(f"Gesamtzucker: {self.calculate_total_sugar()} g")
        print(f"Gesamtkalorien: {self.calculate_total_calories()} kcal")
        print(f"Gesamtkochzeit: {self.calculate_total_cooking_time()} Minuten")
        print(f"Benötigte Utensilien: {self.calculate_total_utens()}")
