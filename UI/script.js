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
        return
    }
    //insert a text box for cities per member
    inputf.innerHTML = "<legend>Each member's starting City:</legend>"
    for (let i = 0; i < numOfMems.value; ++i){
        inputf.innerHTML += "<input type='text' class='startCity'><br>"
    }
    inputf.innerHTML += "Duration In Days:<br>"
    inputf.innerHTML += "<input type='text' id='duration'><br>"
    inputf.innerHTML += "<button type='button' id='submitAll'>Submit</button>"
    //set up for changing the result field
    allSub = document.getElementById("submitAll")
    startCities = document.getElementsByClassName("startCity")
    dur = document.getElementById("duration")
    resultf.innerHTML = "<legend>Results:</legend>"
    allSub.addEventListener("click", function(){
        //stop if no cities provided
        if (startCities.length < 0){
            return
        }
        
        // Create the request body
        let requestBody = {
            startCities: [],
            duration: dur.value
        };

        for (let i = 0; i < startCities.length; i++) {
            requestBody.startCities.push(startCities[i].value);
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
            //set the result field
            resultf.innerHTML = "<legend>Results:</legend>"
            //startCities = data.city
            // for (let i = 0; i < startCities.length; ++i){
            //     resultf.innerHTML += `<div>${startCities[i].value}</div>`
            // }
            resultf.innerHTML += `<div>${data.city}</div>`
            resultf.innerHTML += `<div>${data.cost}</div>`
        })
        .catch(error => {
            // Handle error
            console.error('Error:', error);
        });
    })
})
