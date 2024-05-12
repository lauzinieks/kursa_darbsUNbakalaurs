// Wait for the DOM to fully load
window.addEventListener('DOMContentLoaded', (event) => {
    let footerMenu = document.getElementsByClassName("footer__menu")[0]; // Targeting the specific element
    if (footerMenu) {
        let newListItem = document.createElement('li'); // Creating a new list item
        let inputElement = document.createElement('input'); // Creating the input element
        inputElement.type = 'text';
        inputElement.placeholder = 'Enter something...';
        newListItem.appendChild(inputElement); // Appending the input to the new list item
        footerMenu.appendChild(newListItem); // Appending the new list item to the UL
    } else {
        console.log("Could not find the footer menu.");
    }
});