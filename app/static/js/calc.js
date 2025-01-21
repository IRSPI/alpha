function toggleHeightUnit(unit) {
  const heightSlider = document.getElementById("height-slider");
  const heightInput = document.getElementById("height-input");
  const heightFeetInches = document.getElementById("height-feet-inches");

  if (unit === "cm") {
    heightInput.style.display = "block";
    heightFeetInches.style.display = "none";
  } else {
    heightInput.style.display = "none";
    heightFeetInches.style.display = "block";
  }
}

function toggleWeightUnit(unit) {
  const weightSlider = document.getElementById("weight-slider");
  const weightDisplay = document.getElementById("weight-display");

  if (unit === "kg") {
    weightSlider.min = 10;
    weightSlider.max = 300;
    weightSlider.value = 70;
    updateWeightDisplay();
  } else {
    weightSlider.min = 22;
    weightSlider.max = 660;
    weightSlider.value = 154;
    updateWeightDisplay();
  }
}

function updateHeightDisplay() {
  const heightSlider = document.getElementById("height-slider");
  const heightDisplay = document.getElementById("height-display");
  const feet = document.getElementById("height-feet").value;
  const inches = document.getElementById("height-inches").value;

  if (document.querySelector("input[name='height-unit']:checked").value === "cm") {
    heightDisplay.textContent = `${heightSlider.value} cm`;
  } else {
    heightDisplay.textContent = `${feet} ft ${inches} in`;
  }
}

function updateWeightDisplay() {
  const weightSlider = document.getElementById("weight-slider");
  const weightDisplay = document.getElementById("weight-display");

  if (document.querySelector("input[name='weight-unit']:checked").value === "kg") {
    weightDisplay.textContent = `${weightSlider.value} kg`;
  } else {
    weightDisplay.textContent = `${weightSlider.value} lbs`;
  }
}

function calculateBMI() {
  const heightUnit = document.querySelector("input[name='height-unit']:checked").value;
  const weightUnit = document.querySelector("input[name='weight-unit']:checked").value;
  let height, weight;

  if (heightUnit === "cm") {
    height = parseFloat(document.getElementById("height-slider").value) / 100;
  } else {
    const feet = parseFloat(document.getElementById("height-feet").value) || 0;
    const inches = parseFloat(document.getElementById("height-inches").value) || 0;
    height = (feet * 12 + inches) * 0.0254; // Convert feet and inches to meters
  }

  if (weightUnit === "kg") {
    weight = parseFloat(document.getElementById("weight-slider").value);
  } else {
    weight = parseFloat(document.getElementById("weight-slider").value) * 0.453592; // Convert lbs to kg
  }

  if (!height || !weight) {
    document.getElementById("bmi-result").textContent = "Please provide valid inputs.";
    return;
  }

  const bmi = (weight / (height ** 2)).toFixed(2);
  let category = "";

  if (bmi < 18.5) {
    category = "Underweight";
  } else if (bmi >= 18.5 && bmi < 24.9) {
    category = "Normal weight";
  } else if (bmi >= 25 && bmi < 29.9) {
    category = "Overweight";
  } else {
    category = "Obesity";
  }

  document.getElementById("bmi-result").textContent = `BMI: ${bmi} (${category})`;
}

// Weight Conversion
function convertWeight(reverse = false) {
  const stonesInput = document.getElementById('stones');
  const poundsInput = document.getElementById('pounds');
  const kilogramsInput = document.getElementById('kilograms');

  if (!reverse) {
    const stones = parseFloat(stonesInput.value) || 0;
    const pounds = parseFloat(poundsInput.value) || 0;
    const totalPounds = stones * 14 + pounds;
    const kilograms = (totalPounds * 0.453592).toFixed(2);
    kilogramsInput.value = kilograms;
  } else {
    const kilograms = parseFloat(kilogramsInput.value) || 0;
    const totalPounds = kilograms / 0.453592;
    const stones = Math.floor(totalPounds / 14);
    const pounds = (totalPounds % 14).toFixed(2);
    stonesInput.value = stones;
    poundsInput.value = pounds;
  }
}

// Temperature Conversion
function convertTemperature(reverse = false) {
  const fahrenheitInput = document.getElementById('fahrenheit');
  const celsiusInput = document.getElementById('celsius');

  if (!reverse) {
    const fahrenheit = parseFloat(fahrenheitInput.value) || 0;
    const celsius = ((fahrenheit - 32) * 5 / 9).toFixed(2);
    celsiusInput.value = celsius;
  } else {
    const celsius = parseFloat(celsiusInput.value) || 0;
    const fahrenheit = ((celsius * 9 / 5) + 32).toFixed(2);
    fahrenheitInput.value = fahrenheit;
  }
}

// Height Conversion
function convertHeight(reverse = false) {
  const feetInput = document.getElementById('feet');
  const inchesInput = document.getElementById('inches');
  const centimetersInput = document.getElementById('centimeters');

  if (!reverse) {
    const feet = parseFloat(feetInput.value) || 0;
    const inches = parseFloat(inchesInput.value) || 0;
    const totalInches = feet * 12 + inches;
    const centimeters = (totalInches * 2.54).toFixed(2);
    centimetersInput.value = centimeters;
  } else {
    const centimeters = parseFloat(centimetersInput.value) || 0;
    const totalInches = centimeters / 2.54;
    const feet = Math.floor(totalInches / 12);
    const inches = (totalInches % 12).toFixed(2);
    feetInput.value = feet;
    inchesInput.value = inches;
  }
}
