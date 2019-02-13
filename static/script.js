// Prevent default behavior by showing alert if the inputValue is not a number 
// and/or if the option of the select is not selected
document.querySelector("#form-counter").addEventListener("submit", function (e) {
    const inputValue = document.getElementById("input-value").value; // get input value
    const selectedOption = document.getElementById("action-select-box").value; // get the option selected

    // isFinite will return true if the value is a number even without casting it to string
    if (inputValue === "" || !isFinite(inputValue) || selectedOption === "") {
        alert("Veuillez s'il vous plaît entrer une valeur correcte et choisir une opération.")
        e.preventDefault();
    }
});