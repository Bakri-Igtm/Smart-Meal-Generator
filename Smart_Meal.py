import pandas as pd
import streamlit as st
import base64
import os

recipes_db = pd.read_csv("recipes-output01.csv")
print(recipes_db.head())

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, 'background.jpg')

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_jpeg_as_page_bg(jpeg_file):
    bin_str = get_base64_of_bin_file(jpeg_file)
    page_bg_img = f'''
    <style>
    body {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Call the function with your JPEG image file

# device = "cuda" if torch.cuda.is_available() else "cpu"
# model_id = "runwayml/stable-diffusion-v1-5"
# pipe = StableDiffusionPipeline.from_pretrained(model_id)
# pipe = pipe.to(device)


# def match_recipes(ingredients, recipe_db):
#     matches = []
#     for _, recipe_val in recipe_db.iterrows():
#         recipe_ingredients = recipe_val['RecipeIngredientParts'].split(',')
#         matched_ingredients = set(ingredients).intersection(set(recipe_ingredients))
#         match_score = len(matched_ingredients) / len(recipe_ingredients)
#         if match_score > 0:  # Adjust threshold as needed
#             matches.append((recipe_val, match_score))
#     matches.sort(key=lambda x: x[1], reverse=True)
#     return [s[0] for s in matches]

def match_recipes(ingredients, recipe_db):
    matching_recipes = []
    for _, recipe in recipe_db.iterrows():
        if all(ingredient in recipe['RecipeIngredientParts'] for ingredient in ingredients):
            matching_recipes.append(recipe)
    return matching_recipes

# def generate_image_from_description(description):
#     image = pipe(description).images[0]
#     return image

st.title("Smart Meal Generator")
st.header("Enter the ingredients you have with you")
set_jpeg_as_page_bg('background.jpeg')

ingredients_input = st.text_input("Ingredients (comma separated)")

if st.button("Find Recipes"):
    st.spinner('Processing...')
    if ingredients_input:
        ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",")]
        matching_recipes = match_recipes(ingredients, recipes_db)
        st.write(f"Found {len(matching_recipes)} recipes:")
        number = 1
        for recipe in matching_recipes:
            # print(type(recipe['RecipeInstructions']))
            st.write(f"**{number}. {recipe['Name']}**: ")
            instruction = recipe['RecipeInstructions']
            instruction_list = instruction[1:-1].split('"')
            steps = 1
            # st.write(instruction_list)
            for instruct in instruction_list:
                if instruct and instruct[0] != ",":
                    st.write(f"STEP{steps}: {instruct}")
                    steps += 1
            number += 1
            st.write(" ")
            st.write(" ")
            # st.write(instruction_list[0])

            # instruction.replace(0, "")
            # instruction.replace(-1, "")
            # st.write(recipe['RecipeInstructions'][0])
            # steps = 1
            # for step in recipe['RecipeInstructions']:
            #     st.write(f"STEP {steps}: {recipe['RecipeInstructions'][steps-1]}")
            #     steps += 1
            # steps = 1
    else:
        st.write("Please enter some ingredients.")
    st.success("Done!")
