'use strict';

const fetch = require('node-fetch');
const APIXU_KEY = '110524c6b7b34742afd171954191508';

module.exports.getWeather = async (city) => {
    const response = await fetch(`https://api.apixu.com/v1/current.json?key=${APIXU_KEY}&q=${city}`);
    const data = await response.json();

    console.log(data);
};

module.exports.getForecast = async (city) => {
    const response = await fetch(`https://api.apixu.com/v1/forecast.json?key=${APIXU_KEY}&q=${city}`);

  const data = await response.json();

  console.log(JSON.stringify(data.forecast));
};

// getWeather('Johannesburg');
// weatherForecast('Johannesburg');