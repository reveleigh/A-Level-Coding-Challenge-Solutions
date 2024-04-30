// Function to perform the conversion based on the selected conversion type
function convert() {
    // Retrieve the selected conversion type from the dropdown menu
    const conversionType = document.getElementById('conversionType').value;
    // Retrieve the value entered by the user
    const value = parseFloat(document.getElementById('value').value);
    let result;
  
    // Switch statement to determine the conversion logic based on the selected conversion type
    switch (conversionType) {
        // Convert grams to kilograms
        case 'gramToKg':
            result = value / 1000;
            break;
        // Convert kilograms to grams
        case 'kgToGram':
            result = value * 1000;
            break;
        // Convert USD to Euro using a dummy conversion rate
        case 'usdToEuro':
            result = value * 0.85;
            break;
        // Convert Euro to USD using a dummy conversion rate
        case 'euroToUsd':
            result = value / 0.85;
            break;
        // Convert Celsius to Fahrenheit
        case 'celsiusToFahrenheit':
            result = (value * 9/5) + 32;
            break;
        // Convert Fahrenheit to Celsius
        case 'fahrenheitToCelsius':
            result = (value - 32) * 5/9;
            break;
        // Convert liters to gallons
        case 'literToGallon':
            result = value * 0.264172;
            break;
        // Convert gallons to liters
        case 'gallonToLiter':
            result = value * 3.78541;
            break;
        // Convert USD to GBP using a dummy conversion rate
        case 'usdToGbp':
            result = value * 0.72;
            break;
        // Convert GBP to USD using a dummy conversion rate
        case 'gbpToUsd':
            result = value / 0.72;
            break;
        // Default case for handling invalid conversion types
        default:
            result = 'Invalid conversion type';
    }
  
    // Update the result displayed on the page with the calculated result
    document.getElementById('result').innerText = `Result: ${result}`;
}
