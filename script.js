let numSub = document.getElementById("submitNum")
let numOfMems = document.getElementById("numOfMems")
let inputf = document.querySelector("fieldset")
let allSub = null;
let startCities = null;
let resultf = document.getElementById("results")
numSub.addEventListener("click", function(){
    if(numOfMems.value < 1){
        preventDefault()
    }
    inputf.innerHTML = "<legend>Each member's starting City:</legend>"
    for (let i = 0; i < numOfMems.value; ++i){
        inputf.innerHTML += "<input type='text' class='startCity'><br>"
    }
    inputf.innerHTML += "<button type='botton' id='submitAll'>Submit</button>"
    allSub = document.getElementById("submitAll")
    startCities = document.getElementsByClassName("startCity")
    resultf.innerHTML = "<legend>Results:</legend>"
    allSub.addEventListener("click", function(){
        if (startCities.length < 0){
            preventDefault()
        }
        resultf.innerHTML = "<legend>Results:</legend>"
        for (let i = 0; i < startCities.length; ++i){
            resultf.innerHTML += `<div>${startCities[i].value}</div>`
        }
    })
})

fetch("https://jsonplaceholder.typicode.com/todos", {
  method: "POST",
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  },
  body: JSON.stringify({
    startCities
  })
})
  .then((response) => response.json())
  .then((json) => console.log(json));