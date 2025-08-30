// ===============================
// Configuration
// ===============================
const BASE_URL = "https://house-prediction-w0vn.onrender.com";
// For local testing, uncomment the next line:
// const BASE_URL = "http://127.0.0.1:5000";

// ===============================
// Load locations dynamically when page loads
// ===============================
window.onload = function () {
  fetch(`${BASE_URL}/get_location_names`)
    .then(response => response.json())
    .then(data => {
      const locationList = document.getElementById("location-list");
      data.locations.forEach(loc => {
        let option = document.createElement("option");
        option.value = loc;
        locationList.appendChild(option);
      });
    })
    .catch(() => {
      alert("⚠️ Failed to load locations. Check if the backend is running.");
    });
};

// ===============================
// Validate user inputs
// ===============================
function validateInputs(payload) {
  const currentYear = new Date().getFullYear();
  let errors = [];

  if (payload.total_sqft <= 0) errors.push("Total sqft must be greater than 0.");
  if (payload.bhk <= 0) errors.push("BHK must be at least 1.");
  if (payload.bath <= 0) errors.push("Bathrooms must be at least 1.");
  if (payload.total_sqft / payload.bhk < 300)
    errors.push("Each BHK should have at least 300 sqft.");
  if (payload.bath > payload.bhk + 2)
    errors.push("Too many bathrooms for the given BHK count.");
  if (payload.built_year > currentYear)
    errors.push("Built year cannot be in the future.");

  return errors;
}

// ===============================
// Handle form submission
// ===============================
document.getElementById("price-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const currentYear = new Date().getFullYear();
  const total_sqft = parseFloat(document.getElementById("total_sqft").value) || 0;
  const bhk = parseInt(document.getElementById("bhk").value) || 0;
  const bath = parseInt(document.getElementById("bath").value) || 0;
  const built_year = parseInt(document.getElementById("built_year").value) || currentYear;
  const property_age = currentYear - built_year;

  const payload = {
    total_sqft: total_sqft,
    bath: bath,
    bhk: bhk,
    built_year: built_year,
    property_age: property_age,
    area_type: document.getElementById("area_type").value,
    availability: document.getElementById("availability").value,
    location: document.getElementById("location").value,
    nearby_metro: document.getElementById("nearby_metro").value,
    age_segment: document.getElementById("age_segment").value || "auto",
  };

  // Validate inputs
  const errors = validateInputs(payload);
  const resultElement = document.getElementById("result");
  if (errors.length > 0) {
    resultElement.innerText = "⚠️ " + errors.join("\n⚠️ ");
    resultElement.style.color = "red";
    return;
  }

  // API call to backend
  fetch(`${BASE_URL}/predict_home_price`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then(response => response.json())
    .then(data => {
      resultElement.innerText =
        `Estimated Price: ₹${data.estimated_price_lakhs} Lakhs\n\n` +
        `Description: ${data.description}`;
      resultElement.style.color = "#60A5FA";
    })
    .catch(() => {
      resultElement.innerText = "⚠️ Failed to fetch prediction. Check backend.";
      resultElement.style.color = "red";
    });
});
