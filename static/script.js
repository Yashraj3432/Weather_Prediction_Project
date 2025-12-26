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

        localStorage.setItem("username", username);

        window.location.href = "/dashboard";
        // Redirect to dashboard on successful login
        
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
  const temp = document.getElementById("temp").value;
  const humidity = document.getElementById("humidity").value;
  const wind = document.getElementById("wind").value;

  const response = await fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      temp: Number(temp),
      humidity: Number(humidity),
      wind: Number(wind)
    })
  });

  const data = await response.json();

  if (!response.ok) {
    alert(data.detail || "Prediction failed");
    return;
  }

  document.getElementById("result").innerText =
    `Predicted Temperature: ${data.predicted_temperature.toFixed(2)} °C`;
}

window.predictWeather = predictWeather;
