// ==UserScript==
// @name         ConvertPrice
// @namespace    http://tampermonkey.net/
// @version      2024-01-28
// @description  try to take over the world!
// @author       You
// @match        https://www.dekudeals.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=openuserjs.org
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Get the country from the element's innerText
var country = document.getElementById("navbarCountry1").innerText.split(" ")[1];
console.log(country); // For debugging

// Select the API URL based on the country
var apiUrl;
if (country === 'JP') {
    apiUrl = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/jpy.json';
} else if (country === 'ZA') {
    apiUrl = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/zar.json';
} else if (country === 'AR') {
    apiUrl = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/ars.json';
} else {
    // Handle other cases or set a default
    console.error('Country not supported: ' + country);
}

// Fetch data from the API
fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
        // Determine the currency based on the country
        var currency = country === 'JP' ? 'jpy' : (country === 'ZA' ? 'zar' : 'ars');

        // Extract the exchange rate from the JSON data
        var exchangeRate = data[currency].vnd;

      // Get all elements with the class 'card-badge'
      var cardBadges = document.querySelectorAll('.card-badge');

      // Loop through each card-badge element
      cardBadges.forEach(function(cardBadge) {
        // Get the strong element within each card-badge
        var strongElement = cardBadge.querySelector('strong');

        // Extract the number from the strong element's text content
        var originalPrice = parseFloat(strongElement.textContent.replace(/[^\d.]/g, '').replace('.', ''));
        console.log(originalPrice)

        if (country !== 'JP'){
        	originalPrice = originalPrice / 100
        }
        // Calculate the new price in VND using the fetched exchange rate
        var newPriceVND = originalPrice * exchangeRate;

        // Create a new price element with VND currency and bold formatting
        var newPriceElement = document.createElement('strong');
        if (country == 'AR'){
        	originalPrice = originalPrice * 1.59
        	newPriceElement.innerHTML = '<br>💳  $' + originalPrice.toFixed(0) + '<br>🔁   ₫' + newPriceVND.toFixed(0).replace(/\d(?=(\d{3})+$)/g, '$&,');

        }else{
        	newPriceElement.innerHTML = '<br>🔁   ₫' + newPriceVND.toFixed(0).replace(/\d(?=(\d{3})+$)/g, '$&,');
        }

        // Insert the new price element after the strong element
        strongElement.insertAdjacentElement('afterend', newPriceElement);
      });
    })
    .catch(error => console.error('Error fetching exchange rate:', error));

})();
