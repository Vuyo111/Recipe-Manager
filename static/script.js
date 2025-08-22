const BASE_URL = "/recipes"; // Relative path to Flask backend

// Fetch all recipes and display
async function fetchRecipes() {
    try {
        const res = await fetch(BASE_URL);
        const recipes = await res.json();

        const list = document.getElementById("recipe-list");
        list.innerHTML = "";

        recipes.forEach(recipe => {
            const li = document.createElement("li");

            // Recipe display
            const recipeText = document.createElement("span");
            recipeText.textContent = `${recipe.name} — Ingredients: ${recipe.ingredients.join(", ")}`;
            li.appendChild(recipeText);

            // Edit button
            const editBtn = document.createElement("button");
            editBtn.textContent = "Edit";
            editBtn.addEventListener("click", () => showEditForm(li, recipe, recipeText));
            li.appendChild(editBtn);

            // Delete button
            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Delete";
            deleteBtn.addEventListener("click", async () => {
                const delRes = await fetch(`${BASE_URL}/${recipe.id}`, { method: "DELETE" });
                if (delRes.ok) fetchRecipes();
            });
            li.appendChild(deleteBtn);

            list.appendChild(li);
        });
    } catch (error) {
        console.error("Error fetching recipes:", error);
    }
}

// Add new recipe
const addForm = document.getElementById("add-form");
const errorMsg = document.getElementById("form-error");

addForm.addEventListener("submit", async (e) => {
    e.preventDefault(); // prevent page reload

    const name = document.getElementById("recipe-name").value.trim();
    const ingredients = document.getElementById("recipe-ingredients").value
        .split(",")
        .map(i => i.trim())
        .filter(i => i.length > 0);

    // Basic validation
    if (!name) {
        errorMsg.textContent = "Recipe name cannot be empty.";
        return;
    }
    if (ingredients.length === 0) {
        errorMsg.textContent = "Please provide at least one ingredient.";
        return;
    }

    // Clear error
    errorMsg.textContent = "";

    try {
        const res = await fetch(BASE_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, ingredients })
        });

        if (res.ok) {
            // Clear inputs
            document.getElementById("recipe-name").value = "";
            document.getElementById("recipe-ingredients").value = "";
            fetchRecipes();
        } else {
            const error = await res.json();
            errorMsg.textContent = error.error;
        }
    } catch (error) {
        console.error("Error adding recipe:", error);
    }
});

// Edit recipe
function showEditForm(li, recipe, recipeText) {
    recipeText.style.display = "none";

    const nameInput = document.createElement("input");
    nameInput.value = recipe.name;
    nameInput.style.marginRight = "5px";

    const ingredientsInput = document.createElement("input");
    ingredientsInput.value = recipe.ingredients.join(", ");
    ingredientsInput.style.marginRight = "5px";

    const saveBtn = document.createElement("button");
    saveBtn.textContent = "Save";
    saveBtn.style.backgroundColor = "#2ecc71"; // green
    saveBtn.style.color = "white";
    saveBtn.addEventListener("click", async () => {
        const updatedRecipe = {
            name: nameInput.value,
            ingredients: ingredientsInput.value.split(",").map(i => i.trim())
        };
        await fetch(`${BASE_URL}/${recipe.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedRecipe)
        });
        fetchRecipes();
    });

    const cancelBtn = document.createElement("button");
    cancelBtn.textContent = "Cancel";
    cancelBtn.style.backgroundColor = "#95a5a6"; // gray
    cancelBtn.style.color = "white";
    cancelBtn.addEventListener("click", () => fetchRecipes());

    li.innerHTML = "";
    li.appendChild(nameInput);
    li.appendChild(ingredientsInput);
    li.appendChild(saveBtn);
    li.appendChild(cancelBtn);
}

// Initial load
fetchRecipes();
