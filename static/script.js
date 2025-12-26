function register() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  })
  .then(res => {
    if (!res.ok) throw new Error("User exists");
    return res.json();
  })
  .then(() => {
    alert("Registration successful! Please login.");
    window.location.href = "/";
  })
  .catch(() => alert("User already exists"));
}

window.register = register; // Make sure this line exists!

// ---------- LOGIN ----------
async function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!username || !password) {
        alert("Please enter both username and password");
        return;
    }

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(errorData.detail || "Invalid username or password");
            return;
        }

        // Redirect to dashboard on successful login
        window.location.href = "/dashboard";
    } catch (err) {
        console.error("Login error:", err);
        alert("Server error. Please try again later.");
    }
}

// Expose globally so onclick works
window.login = login;




// Get username from localStorage (set during login)
const username = localStorage.getItem('username');

async function predictWeather() {
    const temp = parseFloat(document.getElementById('temp').value);
    const humidity = parseFloat(document.getElementById('humidity').value);
    const wind = parseFloat(document.getElementById('wind').value);

    if (!temp || !humidity || !wind) {
        alert("Please enter all values!");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/predict?username=${username}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ temp, humidity, wind })
        });

        if (!response.ok) {
            const error = await response.json();
            alert(error.detail || "Error predicting weather");
            return;
        }

        const data = await response.json();
        document.getElementById('result').innerText = 
            `Predicted Temperature: ${data.predicted_temperature.toFixed(2)} °C`;

    } catch (err) {
        console.error(err);
        alert("Error connecting to server");
    }
}
