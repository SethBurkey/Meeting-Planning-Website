let numSub = document.getElementById("submitNum")
let numOfMems = document.getElementById("numOfMems")
let inputf = document.querySelector("fieldset")
let allSub = null
let startCities = null
let dur = null
let resultf = document.getElementById("results")
let allCities = []
//populate all cities with cities from a dictionary in the same directory
fetch('cityDictionary.json')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        let index = 0
        for (let element in data.locations) {
            allCities[element] = data.locations[element]
            index++
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

numSub.addEventListener("click", function(){
    //stop if 0 members provided
    if(numOfMems.value < 1){
        return
    }
    //insert a text box for cities per member
    inputf.innerHTML = "<legend>Each member's starting City:</legend>"
    for (let i = 0; i < numOfMems.value; ++i){
        let temp = "<select class='startCity'>"
        for (city in allCities){
            temp += `<option>${city}</option>`
        }
        temp += "</select><br>"
        inputf.innerHTML += temp
    }
    inputf.innerHTML += "Duration In Days:<br>"
    inputf.innerHTML += "<input type='number' id='duration'><br>"
    inputf.innerHTML += "<button id='submitAll'>Submit</button>"
    //set up for changing the result field
    allSub = document.getElementById("submitAll")
    startCities = document.getElementsByClassName("startCity")
    dur = document.getElementById("duration")
    resultf.innerHTML = "<legend>Results:</legend>"
    allSub.addEventListener("click", function(){        
        // Create the request body
        let requestBody = {
            startCity: [],
            duration: dur.value
        };

        for (let i = 0; i < startCities.length; i++) {
            requestBody.startCity.push(allCities[startCities[i].value].code)
        }
        requestBody = JSON.stringify(requestBody)
        // Send form data to PHP script using fetch
        fetch('../cgi-bin/mainFileSql.cgi', {
            method: 'POST',
            body: requestBody
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            cities = []
            costs = []
            //parse response data
            for (let i = 0; i < data.length; ++i){
                cities[i] = JSON.parse(data[i]).city
                costs[i] = JSON.parse(data[i]).cost
            }
            
            //set the result field
            resultf.innerHTML = "<legend>Results:</legend>"
            for (city in cities){
                resultf.innerHTML += `<div>${city}</div>`
            }
            for (cost in costs){
                resultf.innerHTML += `<div>${cost}</div>`
            }
        })
        .catch(error => {
            // Handle error
            console.error('Error:', error);
        });
    })
})
