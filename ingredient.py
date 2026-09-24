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

