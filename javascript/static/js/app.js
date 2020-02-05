//previewing the data



var tableData = data;
console.log(data)

function createTable(filteredData){
    var tbody = d3.select("tbody");

    filteredData.forEach((incident) => {
        var row = tbody.append("tr");
        Object.entries(incident).forEach(([key, value]) => {
            if(key != "comments") {
                var cell = row.append("td");
                cell.text(value);
            } else {
                var subrow = tbody.append("tr");
                subrow.append("td");
                subrow.append("td")
                    .attr("colspan", 5)
                    .text(value);
            };
        });
    });
}


//------------------------------------------------------------------
//creating the filter button



//Select the button element on html file
var button = d3.select("#filter-btn");

//take the input from the user and filter the data 
button.on("click", function() {

    // Select the input element 
    var inputElement = d3.select("#datetime");
  

    // Get the date from input
    var userInput = inputElement.property("value");
 
        




    //use tabledata.filter to create the filtered data for the previous function to work
    var filteredTable = tableData.filter(sighting => sighting.datetime === userInput);
    // displayed only the filtered data

    var tbody = d3.select("tbody");
    tbody.html("");
    console.log(filteredTable);
    createTable(filteredTable)
    
 });


createTable(data);
