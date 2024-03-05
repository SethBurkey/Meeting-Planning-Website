let numSub = document.getElementById("submitNum")
let numOfMems = document.getElementById("numOfMems")
let inputf = document.querySelector("fieldset")
let allSub = null
let startCities = null
let dur = null
let resultf = document.getElementById("results")
numSub.addEventListener("click", function(){
    //stop if 0 members provided
    if(numOfMems.value < 1){
        preventDefault()
    }
    //insert a text box for cities per member
    inputf.innerHTML = "<legend>Each member's starting City:</legend>"
    for (let i = 0; i < numOfMems.value; ++i){
        inputf.innerHTML += "<input type='text' class='startCity'><br>"
    }
    inputf.innerHTML += "Duration In Days:<br>"
    inputf.innerHTML += "<input type='text' id='duration'><br>"
    inputf.innerHTML += "<button id='submitAll'>Submit</button>"
    //set up for changing the result field
    allSub = document.getElementById("submitAll")
    startCities = document.getElementsByClassName("startCity")
    dur = document.getElementById("duration")
    resultf.innerHTML = "<legend>Results:</legend>"
    allSub.addEventListener("click", function(){
        //stop if no cities provided
        if (startCities.length < 0){
            preventDefault()
        }
        // URL endpoint for your server
        const url = 'https://john.cedarville.edu';

        // Create the request body
        let requestBody = [];

        for (let i = 0; i < startCities.length; i++) {
            requestBody[i] = JSON.stringify(startCities[i].value);
        }
        requestBody[startCities.length] = dur.value

        // Fetch POST request
        fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: requestBody,
        })
        .then(response => {
            if (!response.ok) {
            throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response:', data);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });

        //set the result field
        resultf.innerHTML = "<legend>Results:</legend>"
        for (let i = 0; i < startCities.length; ++i){
            resultf.innerHTML += `<div>${startCities[i].value}</div>`
        }
        resultf.innerHTML += `<div>${dur.value}</div>`
    })
})
