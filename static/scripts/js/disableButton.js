window.addEventListener('load', (event) => {

    var queryTextBox = document.getElementById("query");

    queryTextBox.addEventListener("input", unlockButton);
});

function unlockButton(e) {
    if(document.getElementById("query").value != "") {
        document.getElementById("start").disabled = false;
    }
    else {
        document.getElementById("start").disabled = true;
    };
};
