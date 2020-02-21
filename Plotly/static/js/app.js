function buildMetadata(sample) {

  // @TODO: Complete the following function that builds the metadata panel

  // Use `d3.json` to fetch the metadata for a sample
  
  var url = `/metadata/${sample}`;
  d3.json(url).then(function(sample){
    console.log(sample);

    // Use d3 to select the panel with id of `#sample-metadata`
      var selector = d3.select("#sample-metadata");
    
    // Use `.html("") to clear any existing metadata
    selector.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
    Object.entries(sample).forEach(([key,value]) => {
      selector.append("p").text(`${key}: ${value}`)
    });

  });
}

function buildCharts(sample) {

    // @TODO: Use `d3.json` to fetch the sample data for the plots
    d3.json(`./samples/${sample}`).then(sample_data => {
        graph_data = Object.entries(sample_data)
        console.log(graph_data)
        
        // @TODO: Build a Pie Chart
        // HINT: You will need to use slice() to grab the top 10 sample_values,
        // otu_ids, and labels (10 each).
        var data = [{
            type: 'pie',
            values: graph_data[2][1].slice(0,10),
            labels: graph_data[0][1].slice(0,10),
            hovertext: graph_data[1][1].slice(0,10),
            automargin: true
        }];

        var layout = {
            height: 400,
            width: 400,
            margin:{"t": 25, "b": 0, "l": 0, "r": 0}
        };

        Plotly.newPlot('pie', data, layout);

        // @TODO: Build a Bubble Chart using the sample data
        var desired_maximum_marker_size = 40;
        var size = [400, 600, 800, 1000];
        var trace = {
          x: graph_data[0][1],
          y: graph_data[2][1],
          text: graph_data[1][1],
          mode: 'markers',
          marker: {
            colorscale: 'Earth',
            color: graph_data[0][1],
            size: graph_data[2][1],
          }
        };

        var data = [trace];

        var layout = {
          height: 500,
          width: 1250,
          x_label: 'OTU ID',
          xaxis: {
            title: "OTU ID",
            range: [0, graph_data[0][1]]
          },
          yaxis: {
            range: [0, 350]
          },
          showlegend: false
        };

        Plotly.newPlot('bubble', data, layout);    
    });
}



function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();