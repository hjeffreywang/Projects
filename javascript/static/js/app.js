//previewing the data



var tableData = data;
console.log(data)

// Use d3 to choose the tbody in html, and fill table with data
var tbody = d3.select("tbody");

// appends all the data from data.js file into the html page
data.forEach((sighting) => {
    //add a new row for each grouping of data
    var row = tbody.append("tr");
    Object.entries(sighting).forEach(([key, value]) => {
      var cell = tbody.append("td");
      cell.text(value);
    });
});


//------------------------------------------------------------------
//creating the filter button



//Select the button element on html file
var button = d3.select("#filter-btn");

//take the input from the user and filter the data 
button.on("click", function() {

    // Select the input element 
    var inputElement = d3.select("#datetime");
  

    // Get the value the input
    var userInput = inputElement.property("value");
 
    // Prevent refreshing
    d3.event.preventDefault();




    //use the tabledata filter to create the filtered information
    var filteredTable = tableData.filter(sighting => sighting.datetime === userInput);
    tbody.html("");
    
    // displayed only the filtered data
    filteredTable.forEach((sighting) => {
        console.log(filteredTable);
        var row = tbody.append("tr");
        Object.entries(sighting).forEach(([key, value]) => {
          var cell = tbody.append("td");
          cell.text(value);
        });

    });
 });



