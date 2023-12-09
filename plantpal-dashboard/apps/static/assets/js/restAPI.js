const DAY = 86400;
const MONTH = 2629743;
const YEAR = 31556926;
const TIMEOUT_INTERVAL = 30000;
let waterVolume = getWaterVolume();
let time;

window.addEventListener('load', function () {
    getDailyUsage();
    getMonthlyUsage();
    getYearlyUsage();
    getWaterLevel();
    setInterval(function () {
        getDailyUsage();
        getMonthlyUsage();
        getYearlyUsage();
        getWaterLevel();
    }, TIMEOUT_INTERVAL);

    getTTL();
}, false)

function getWaterVolume() {
    fetch('/API/contCapacity?plantID=1', {method: "GET"})
        .then(r => r.json())
        .then(data => {
            waterVolume = data[0].waterVolume;
        });
}

function getDailyUsage() {
    fetchUsage(DAY, "dailyUse", "dailyUsePercent");
}

function getMonthlyUsage() {
    fetchUsage(MONTH, "monthlyUsage", null);
}

function getYearlyUsage() {
    fetchUsage(YEAR, "yearUsage", null);
}

function getWaterLevel() {
    fetch(getSensorURL(1, "LoadCell"), {method: "GET"})
        .then(r => r.json())
        .then(data => {
            let level = data["LoadCell"][0].value;
            let percent = Math.floor(level / waterVolume * 100);
            document.getElementById("WLevel").innerHTML = level.toFixed(2) + "<sub class=\"text-muted f-14\">Liters</sub>";
            document.getElementById("WLevelPercent").innerText = percent + "%";

            if(level < 0.4) {
                new Notification("Please add more water to the plant!");
            }
        })
}

function getTTL() {
    fetch('/API/PlantCount', {method: 'GET'})
        .then(r => r.json())
        .then(data => {
            document.getElementById('PlantPalNr').innerText = data[0].PlantPals;
        });
    fetch('/API/LastWater?plantID=1', {method: 'GET'})
        .then(r => r.json())
        .then(data => {
            time = new Date(data[0].time * 1000);
            document.getElementById('timeElapsed').innerText = new Date(time).toISOString().substr(11, 8);

            setInterval(function () {
                time.setSeconds(time.getSeconds() + 1);
                document.getElementById('timeElapsed').innerText = new Date(time).toISOString().substr(11, 8);
            }, 1000);
        })
}

/*
    UTILITY
 */

function getSensorURL(limit, type) {
    if (type === null) {
        throw new Error("No Type defined");
    }

    let url = '/API/sensorData?plantID=1&type=' + type;

    if (limit !== null) {
        url += '&limit=' + limit;
    }

    return url;
}

function getHistoryURL(seconds) {
    let url = '/API/historicalData?plantID=1';
    if (seconds > 0)
        url += '&date=' + seconds;

    return url;
}

function sumUsage(data) {
    let result = 0;
    for (let d of data) {
        result += d.amount;
    }

    return result;
}

function fetchUsage(timeFrame, useTag, percentageTag) {
    fetch(getHistoryURL(timeFrame), {method: 'GET'})
        .then(response => response.json())
        .then(data => {
            let result = sumUsage(data);

            document.getElementById(useTag).innerText = result + " liters";
            if (percentageTag !== null) {
                let percentage = Math.floor((result / waterVolume) * 100);
                document.getElementById(percentageTag).innerText = percentage + " %";
            }

        });
}