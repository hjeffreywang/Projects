//setup 
var svgWidth = 920;
var svgHeight = 500;

var margin = {
  top: 20,
  right: 40,
  bottom: 80,
  left: 100
};

// Create a SVG wrapper that appends an SVG group that will hold our chart,
// and shift the latter by left and top margins
var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;



// Create the SVG wrapper, append an SVG group to hold 
// the chart group and shift the chart over
var svg = d3.select("#scatter")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);


var chartGroup = svg.append("g")
	.attr("transform", `translate(${margin.left}, ${margin.top})`);


//create functions


//function used for updating circles group with new tooltip
function updateToolTip(chosenXAxis, chosenYAxis, circlesGroup, statesGroup) {
  if (chosenXAxis === "income") {
    var xlabel = "Income: ";
    var xsuf = "";
  };
  if (chosenXAxis === "age") {
    var xlabel = "Age: ";
    var xsuf = "";
  };
  if (chosenXAxis === "poverty") {
    var xlabel = "Poverty: ";
    var xsuf = "%";
  };

  if (chosenYAxis === "healthcare") {
    var ylabel = "Uninsured: ";
    var ysuf = "%";
  };
  if (chosenYAxis === "smokes") {
    var ylabel = "Smokes: ";
    var ysuf = "%";
  };
  if (chosenYAxis === "obesity") {
    var ylabel = "Obesity: ";
    var ysuf = "%";
  };

  var toolTip = d3.tip()
    .attr("class", "d3-tip")
    .offset([-8, 0])
    .html(function(d) {
      return (`${d.state}<br>${xlabel}: ${d[chosenXAxis]}${xsuf}<br>${ylabel}: ${d[chosenYAxis]}${ysuf}`);
    });
  svg.call(toolTip);
    
  circlesGroup
    .on("mouseover", function(data) {
      toolTip.show(data);
    })
    // onmouseout event
    .on("mouseout", function(data, index) {
      toolTip.hide(data);
    });

  statesGroup
    .on("mouseover", function(data) {
      toolTip.show(data);
    })
    // onmouseout event
    .on("mouseout", function(data, index) {
      toolTip.hide(data);
    });
    
  return circlesGroup;
}








//Actual Data reading and processing



// Import Data 
// must create local server to load
var file = "assets/data/data.csv"


// Function is called and passes csv data
d3.csv(file).then(function(data) {
  //console log to see the data
  console.log(data);

    data.forEach(d => {
      d.smokes = +d.smokes;
      d.age = +d.age;
    });


      //  Create scale functions
  // Linear Scale takes the min to be displayed in axis, and the max of the data
  var xLinearScale = d3.scaleLinear()
    .domain([30, d3.max(data, d => d.age)])
    .range([0, width]);

  var yLinearScale = d3.scaleLinear()
    .domain([8, d3.max(data, d => d.smokes)])
    .range([height, 0]);

  // Create axis functions by calling the scale functions
  var bottomAxis = d3.axisBottom(xLinearScale);
  var leftAxis = d3.axisLeft(yLinearScale);

  // Append the axes to the chart group 
  chartGroup.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(bottomAxis);
  
  // Only append the left axis 
  chartGroup.append("g")
    .call(leftAxis);

  // Styling
  chartGroup.select('.domain').attr('stroke', 'blue')  // '.domain' is the main axis line <path> element
  chartGroup.selectAll('.tick line')  // '.tick' is the <g> element of ticks, and <line> and <text> are in it
    .attr('stroke', 'teal')
  chartGroup.select('.tick:first-of-type text').remove() // 'first-of-type' and 'last-of-type'
  chartGroup.selectAll('.tick text')
    .attr('font-size', 12)
    .attr('font-family', 'serif')
    .attr('fill', 'blue')




  // Create Circles
  var circlesGroup = chartGroup.selectAll("circle")
    .data(data)
    .enter()

  var circles = circlesGroup.append("circle")
    .attr("cx", d => xLinearScale(d.age))
    .attr("cy", d => yLinearScale(d.smokes) -4)
    .attr("r", "12")
    .attr("fill", "#45B6CE")
    .attr("opacity", ".65");


  // Append text to circles 
  var circleLabel = circlesGroup.append("text")
    .attr("x", d => xLinearScale(d.age))
    .attr("y", d => yLinearScale(d.smokes))
    .style("font-size", "12px")
    .style("text-anchor", "middle")
    .style("fill", "white")
    .text(d => d.abbr);

  // Initialize tool tip
    var toolTip = d3.tip()
      .attr("class", "d3-tip")
      .html(function(d) {
        return (`State: ${d.abbr}<br>Smoker: ${d.smokes}%<br>Age (Med): ${d.age}`);
    });

  // Create tooltip in the chart
  
  chartGroup.call(toolTip);

  // Create event mouseover event
  circles.on("mouseover", function (data) {
    toolTip.show(data, this);
  })
    //  event on mouseing out


    .on("mouseout", function (data) {
      toolTip.hide(data, this);
    });

  // labels for axes
  chartGroup.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left + 5)
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .attr("class", "axisText")
    .text("Smoker (%)");

  chartGroup.append("text")
    .attr("transform", `translate(${width / 2}, ${height + margin.top + 20})`)
    .attr("class", "axisText")
    .text("Age (Median)");
});