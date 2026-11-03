from flask import Flask, render_template, request, redirect, url_for
import pickle as pickle
import base64
import urllib.request

from security import encrypt_data, decrypt_data, EncryptionError, is_url_scheme_allowed

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        ingredients = request.form['ingredients']
        secret_ingredient = request.form['secret_ingredient']

        recipe = {
            'recipe_name': recipe_name,
            'ingredients': ingredients,
            'secret_ingredient': secret_ingredient
        }

        serialized_recipe = pickle.dumps(recipe)
        encrypted_recipe = encrypt_data(serialized_recipe)
        return render_template('encrypted_data.html', data=encrypted_recipe)

    return render_template('submit_recipe.html')

@app.route('/view', methods=['GET', 'POST'])
def view_recipe():
    if request.method == 'POST':
        encrypted_recipe = request.form.get('encrypted_data', '')
        recipe_url = request.form.get('url')

        if recipe_url:
            if not is_url_scheme_allowed(recipe_url):
                return "URL scheme not allowed", 400
            try:
                print(recipe_url,flush=True)
                with urllib.request.urlopen(recipe_url) as response:
                    encrypted_recipe = response.read().decode('utf-8').strip()
            except Exception as e:
                return f"Unable to retrieve recipe data", 400

        if not encrypted_recipe:
            return "Invalid request!", 400

        try:
            encrypted_recipe = encrypted_recipe.encode('utf-8')
            serialized_recipe = decrypt_data(encrypted_recipe, None)
            recipe = pickle.loads(serialized_recipe)
            return render_template('view_recipe.html', recipe=recipe)
        except EncryptionError:
            return "Encryption key misconfigured", 500
        except Exception:
            return f"Error loading recipe. Please check:\n{encrypted_recipe}", 500

    return render_template('view_recipe_form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)
