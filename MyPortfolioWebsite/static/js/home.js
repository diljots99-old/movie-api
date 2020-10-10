function myFunction() {
    var x = document.getElementById("mynav_bar");
    if (x.className === "nav_bar") {
        x.className += " responsive";
    } else {
        x.className = "nav_bar";
    }
}