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
        self.cooking_time = serving[-2]
        self.utensils = serving[-1]

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
        self.read_data()

    def read_data(self):
        self.cooking_time1 = self.serving_1.cooking_time
        self.cooking_time2 = self.serving_2.cooking_time
        self.protein1 = self.serving_1.protein
        self.protein2 = self.serving_2.protein
        self.fat1 = self.serving_1.fat
        self.fat2 = self.serving_2.fat
        self.carbohydrates1 = self.serving_1.carbs
        self.carbohydrates2 = self.serving_2.carbs
        self.fiber1 = self.serving_1.fiber
        self.fiber2 = self.serving_2.fiber
        self.sugar1 = self.serving_1.sugar
        self.sugar2 = self.serving_2.sugar
        self.calories1 = self.serving_1.calories
        self.calories2 = self.serving_2.calories
        self.utens1 = self.serving_1.utensils
        self.utens2 = self.serving_2.utensils

        self.total_protein = (
            self.protein1 * self.gram_1 / 100 
            + self.protein2 * self.gram_2 / 100
        )

        self.total_fat = (
            self.fat1 * self.gram_1 / 100 
            + self.fat2 * self.gram_2 / 100
        )

        self.total_carbohydrates = (
            self.carbohydrates1 * self.gram_1 / 100 
            + self.carbohydrates2 * self.gram_2 / 100
        )

        self.total_fiber = (
            self.fiber1 * self.gram_1 / 100
            + self.fiber2 * self.gram_2 / 100
        )

        self.total_sugar = (
            self.sugar1 * self.gram_1 / 100
            + self.sugar2 * self.gram_2 / 100
        )

        self.total_calories = (
            self.calories1 * self.gram_1 / 100
            + self.calories2 * self.gram_2 / 100
        )

        self.total_utens = self.utens1 + self.utens2

        self.total_cooking_time = self.cooking_time1 + self.cooking_time2
    
    def show_meal_info(self):
        print(f"Gesamtprotein: {self.total_protein} g")
        print(f"Gesamtfett: {self.total_fat} g")
        print(f"Gesamtkohlenhydrate: {self.total_carbohydrates} g")
        print(f"Gesamtballaststoffe: {self.total_fiber} g")
        print(f"Gesamtzucker: {self.total_sugar} g")
        print(f"Gesamtkalorien: {self.total_calories} kcal")
        print(f"Gesamtkochzeit: {self.total_cooking_time} Minuten")
        print(f"Benötigte Utensilien: {self.total_utens}")
