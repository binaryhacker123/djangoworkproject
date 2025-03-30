// Energy Calculator Calculation Logic

// Conversion factors and constants
const ENERGY_FACTORS = {
    heating: {
        'natural-gas': 1.1, // CO2 kg per kWh
        'electric': 0.5,    // Varies by region, using average
        'oil': 0.9,
        'propane': 1.3,
        'heat-pump': 0.3    // More efficient
    },
    vehicle: {
        'gas': 0.404,       // kg CO2 per mile
        'diesel': 0.45,
        'hybrid': 0.25,
        'electric': 0.1,    // Depends on electricity source
        'none': 0
    },
    averageMonthlyEnergyUsage: 850, // kWh for average US household
    averageAnnualCarbonFootprint: 16 // tons CO2 per person
};

function calculateEnergyUsage(formData) {
    let energyComponents = {
        baseUsage: ENERGY_FACTORS.averageMonthlyEnergyUsage,
        heatingImpact: 0,
        vehicleImpact: 0,
        efficiencyReduction: 0
    };

    // Adjust base usage by household size
    energyComponents.baseUsage *= (formData.householdSize / 2);

    // Adjust based on home size
    energyComponents.baseUsage *= (formData.homeSize / 1200);

    // Heating energy impact
    energyComponents.heatingImpact = ENERGY_FACTORS.heating[formData.heatingType] * 
        (formData.coolingMonths / 6) * 200;

    // Vehicle energy impact
    energyComponents.vehicleImpact = ENERGY_FACTORS.vehicle[formData.vehicleType] * 
        formData.milesDriven * 52 / 1000;

    // Efficiency reduction from energy-efficient appliances
    const efficientAppliancesCount = formData.efficientAppliances.length;
    energyComponents.efficiencyReduction = efficientAppliancesCount * 50;

    // Renewable energy adjustment
    const renewableAdjustment = formData.renewableEnergy ? 0.5 : 1;

    // Total energy calculation
    const totalEnergyUsage = Math.round(
        (energyComponents.baseUsage + 
         energyComponents.heatingImpact + 
         energyComponents.vehicleImpact - 
         energyComponents.efficiencyReduction) * 
        renewableAdjustment
    );

    // Carbon footprint calculation
    const carbonFootprint = Math.round(
        (totalEnergyUsage / 850) * 
        ENERGY_FACTORS.averageAnnualCarbonFootprint * 
        renewableAdjustment
    );

    // Compare to average
    const comparisonToAverage = Math.round(
        ((ENERGY_FACTORS.averageAnnualCarbonFootprint - carbonFootprint) / 
         ENERGY_FACTORS.averageAnnualCarbonFootprint) * 100
    );

    return {
        energyUsage: totalEnergyUsage,
        carbonFootprint: carbonFootprint,
        comparisonToAverage: comparisonToAverage,
        recommendations: generateRecommendations(formData, carbonFootprint)
    };
}

function generateRecommendations(formData, carbonFootprint) {
    const recommendations = [];

    if (carbonFootprint > 10) {
        recommendations.push("Consider switching to solar power to reduce your electricity carbon footprint.");
    }

    if (formData.heatingType !== 'heat-pump') {
        recommendations.push("Upgrading to a heat pump could save approximately 30% on your heating costs.");
    }

    if (formData.efficientAppliances.length < 2) {
        recommendations.push("Energy-efficient appliances could reduce your energy consumption by up to 20%.");
    }

    if (formData.vehicleType === 'gas' || formData.vehicleType === 'diesel') {
        recommendations.push("Consider transitioning to a hybrid or electric vehicle to significantly reduce transportation emissions.");
    }

    return recommendations;
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('energy-calculator');
    const calculateBtn = document.getElementById('calculate-btn');
    const resultsSection = document.getElementById('results');

    // Update cooling months display
    document.getElementById('cooling-months').addEventListener('input', function() {
        document.getElementById('cooling-months-value').textContent = this.value;
    });

    calculateBtn.addEventListener('click', () => {
        const formData = {
            householdSize: parseInt(document.getElementById('household-size').value),
            homeSize: parseInt(document.getElementById('home-size').value),
            electricityBill: parseFloat(document.getElementById('electricity-bill').value),
            renewableEnergy: document.getElementById('renewable-yes').checked,
            heatingType: document.getElementById('heating-type').value,
            coolingMonths: parseInt(document.getElementById('cooling-months').value),
            vehicleType: document.getElementById('vehicle-type').value,
            milesDriven: parseInt(document.getElementById('miles-driven').value),
            efficientAppliances: Array.from(
                document.querySelectorAll('input[name="efficient-appliances"]:checked')
            ).map(checkbox => checkbox.value)
        };

        const results = calculateEnergyUsage(formData);

        // Update results display
        document.querySelector('#results .result-item:nth-child(1) .result-value').textContent = 
            `${results.energyUsage} kWh`;
        document.querySelector('#results .result-item:nth-child(2) .result-value').textContent = 
            `${results.carbonFootprint} tons CO₂ per year`;
        document.querySelector('#results .result-item:nth-child(3) .result-value').textContent = 
            `${Math.abs(results.comparisonToAverage)}% ${results.comparisonToAverage > 0 ? 'lower' : 'higher'}`;

        // Update recommendations
        const recommendationList = document.querySelector('.recommendation-list');
        recommendationList.innerHTML = results.recommendations.map(rec => 
            `<li><i class="fas fa-check-circle"></i><span>${rec}</span></li>`
        ).join('');

        // Show results section
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({behavior: 'smooth'});
    });
});