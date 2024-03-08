/*
 * Meeting Planning Website JavaScript
 * By LightSys - Stache Overflow
 * 
 * This file displays all the possible airports
 * in one drop down per member. Once all the
 * dropdown airports are selected, it then queries
 * an algorithm to find the best meeting location
 * based on where each member is starting from.
 * Lastly it displays the result of the algorithm.
 */
let numSub = document.getElementById("submitNum")
let numOfMems = document.getElementById("numOfMems")
let inputf = document.getElementById('dropdowns')
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
    inputf.innerHTML = "<legend>Each Member's Airport:</legend>"
    for (let i = 0; i < numOfMems.value; ++i){
        let temp = "<select class='startCity'>"
        temp += "<option></option>"
        for (city in allCities){
            temp += `<option>${city}</option>`
        }
        temp += "</select><br>"
        inputf.innerHTML += temp
    }
    inputf.innerHTML += "Duration In Days:<br>"
    inputf.innerHTML += "<input type='number' id='duration' required><br>"
    inputf.innerHTML += "<button id='submitAll'>Submit</button>"
    //set up for changing the result field
    allSub = document.getElementById("submitAll")
    startCities = document.getElementsByClassName("startCity")
    dur = document.getElementById("duration")
    resultf.innerHTML = "<legend>Results:</legend>"
    allSub.addEventListener("click", function(){  
        if (dur.value == '' || dur.value == '0'){
            resultf.innerHTML = "<legend>Destination:</legend>"
            alert("Duration Required")
            return
        }      
        // Create the request body
        let requestBody = {
            startCity: [],
            duration: dur.value
        };
        //populate the request body
        for (let i = 0; i < startCities.length; i++) {
            if(startCities[i].value != ''){
                requestBody.startCity.push(allCities[startCities[i].value].code)
            }
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
            //parse response data
            data = JSON.parse(data)
            if(data.error){
                //inputf.innerHTML = "<legend>Each Member's Airport:</legend>"
                inputf.innerHTML += `<div>Error: ${data.error}</div>`
                return
            }
            cities = []
            costs = []
            //populate cities and costs with the result data
            for (let element in data){
                cities.push(element)
                costs.push(data[element].toFixed(2))
            }            
            //get the detailedName of the city from the Abbriviation (code)
            for(i in cities){
                for (let city in allCities){
                    if(allCities[city].code == cities[i])
                    cities[i] = city
                }
            }
            //set the result field
            let tempRes = "<legend>Destination:</legend>"
            tempRes += "<div id='rgrid'>"
            for (let i = 0; i < costs.length; ++i){
                tempRes += `<div>#${i+1} City: ${cities[i]}</div>`
                tempRes += `<div>#${i+1} Cost: $${costs[i]}</div>`
            }
            tempRes += "</div>"
            resultf.innerHTML = tempRes
        })
        .catch(error => {
            // Handle error
            console.error('Error:', error);
        });
    })
})