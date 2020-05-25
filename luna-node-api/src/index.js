'use strict';

const program = require('commander');
const weather = require('./commands');

program
    .version('0.0.1')
    .description('The beginning of something beautiful')

program
    .command('now <city>')
    .alias('n')
    .description('Get the current weather at a specified city')
    .action(city => weather.getWeather(city));

program
    .command('forecast <city>')
    .alias('f')
    .description('Get the weather forecast for a specified city')
    .action(city => weather.getForecast(city));

program.parse(process.argv);