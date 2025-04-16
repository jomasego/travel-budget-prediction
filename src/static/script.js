document.addEventListener('DOMContentLoaded', function() {
    const predictionForm = document.getElementById('prediction-form');
    const resultsDiv = document.getElementById('results');
    // Get specific result paragraphs
    const predictionHotelP = document.getElementById('prediction-hotel');
    const predictionFoodP = document.getElementById('prediction-food');
    const predictionActivityP = document.getElementById('prediction-activity');
    const modelParamsP = document.getElementById('model-parameters');
    const errorMessageDiv = document.getElementById('error-message');

    // --- Get Unique Values for Dropdowns (optional but good UX) ---
    // This part would ideally fetch unique 'Country' and 'Trip Duration Category'
    // values from the backend or have them pre-defined.
    // For simplicity, we'll pre-define some common values here.

    const countries = [
        "France", "Spain", "Italy", "Germany", "United Kingdom", 
        "USA", "Japan", "Australia", "Thailand", "Other"
        // Add more or fetch dynamically if needed
    ];
    const tripDurations = [
        "Short (1-3 days)",
        "Medium (4-6 days)",
        "Long (7-10 days)",
        "Extended (11+ days)",
        "Missing" // Handle potential missing category
    ];

    const countrySelect = document.getElementById('country');
    const durationSelect = document.getElementById('trip-duration');

    countries.forEach(country => {
        const option = document.createElement('option');
        option.value = country;
        option.textContent = country;
        countrySelect.appendChild(option);
    });

    tripDurations.forEach(duration => {
        const option = document.createElement('option');
        option.value = duration;
        option.textContent = duration;
        durationSelect.appendChild(option);
    });
    // --- End Dropdown Population ---


    predictionForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission
        resultsDiv.style.display = 'none'; // Hide previous results
        errorMessageDiv.style.display = 'none'; // Hide previous errors

        // Get form data
        const formData = new FormData(predictionForm);
        const data = {};
        // Manually map form names to expected API keys
        data['# Adults'] = parseInt(formData.get('adults'), 10);
        data['# Children & Babies'] = parseInt(formData.get('children'), 10);
        data['Trip Duration Category'] = formData.get('trip-duration');
        data['Country'] = formData.get('country');

        // Handle checkboxes - send 1 if checked, 0 otherwise
        const themeFeatures = [
            'Theme Parks', 'Hidden Gems', 'Cultural Attractions',
            'Beach or Pools', 'Sunset Spots', 'Nature Getaway'
        ];
        themeFeatures.forEach(feature => {
            const checkbox = predictionForm.elements[feature]; // Access by name
            data[feature] = checkbox.checked ? 1 : 0;
        });

        console.log('Sending data:', data);

        // Basic validation (ensure numbers are valid)
        if (isNaN(data['# Adults']) || isNaN(data['# Children & Babies'])) {
             showError('Please enter valid numbers for Adults and Children.');
             return;
        }

        // Send data to the /predict endpoint
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) {
                // Try to parse error message from backend
                return response.json().then(err => {
                    throw new Error(err.error || `HTTP error! status: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(result => {
            console.log('Prediction result:', result);
            // Display the predictions
            const predictions = result.predicted_budgets;
            predictionHotelP.textContent = `Predicted Hotel Budget: €${predictions['Hotel Budget in EUR'].toFixed(2)}`;
            predictionFoodP.textContent = `Predicted Food Budget: €${predictions['Food Budget in EUR'].toFixed(2)}`;
            predictionActivityP.textContent = `Predicted Activity Budget: €${predictions['Activity Budget in EUR'].toFixed(2)}`;

            // Display the input parameters used for the prediction
            // Construct parameters string dynamically
            let paramsUsed = `Adults=${data['# Adults']}, Children=${data['# Children & Babies']}, Duration=${data['Trip Duration Category']}, Country=${data['Country']}`;
            themeFeatures.forEach(feature => {
                if (data[feature] === 1) { // Only show selected interests
                    paramsUsed += `, ${feature}`; 
                }
            });
            modelParamsP.textContent = `Based on: ${paramsUsed}`;

            resultsDiv.style.display = 'block'; // Show results
        })
        .catch(error => {
            console.error('Error:', error);
            showError(`Prediction failed: ${error.message}`);
        });
    });

    function showError(message) {
        errorMessageDiv.textContent = message;
        errorMessageDiv.style.display = 'block';
    }
});
