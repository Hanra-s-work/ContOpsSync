function shift_colour() {
    var light = "Light",
        dark = "Dark"
    var element = document.getElementById("body_styling")
    var button_text = document.getElementById("theme_button_id")
    if (button_text.text === dark) {
        element.className = "body_style_light"
        button_text.text = light
    } else {
        element.className = "body_style_dark"
        button_text.text = dark
    }
}

function dynamic_greeting() {
    // Get the current hour of the day (0-23)
    var currentHour = new Date().getHours();
    var greetingMessage = "";

    if (currentHour >= 5 && currentHour < 12) {
        greetingMessage = "Good morning!";
    } else if (currentHour >= 12 && currentHour < 18) {
        greetingMessage = "Good afternoon!";
    } else {
        greetingMessage = "Good evening!";
    }

    // Display the dynamic greeting on the webpage
    document.getElementById('greeting').textContent = greetingMessage;
}

