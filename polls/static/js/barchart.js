function colourScale(value, maxValue) {
    const success = [25, 135, 84];    
    const secondary = [173, 181, 189]; 

    const ratio = 1 - (value / maxValue); // Closer to 0 → greener; closer to 1 → gray

    const r = Math.round(success[0] + (secondary[0] - success[0]) * ratio);
    const g = Math.round(success[1] + (secondary[1] - success[1]) * ratio);
    const b = Math.round(success[2] + (secondary[2] - success[2]) * ratio);

    return `rgb(${r}, ${g}, ${b})`;
}


const dataset = JSON.parse(document.getElementById('chart-data').textContent);
const labels = JSON.parse(document.getElementById('chart-labels').textContent);

var container = document.getElementById("chart");
var w = container.clientWidth;
var h = 200;
var barPadding = 1;

var maxData = d3.max(dataset);
var barWidth = w / dataset.length;

var svg = d3.select("#chart")
    .append("svg")
    .attr("width", w)
    .attr("height", h + 40);

// Create the bars
svg.selectAll("rect")
    .data(dataset)
    .enter()
    .append("rect")
    .attr("x", (d, i) => i * barWidth)
    .attr("y", h)  
    .attr("width", barWidth - barPadding)
    .attr("height", 0)  
    .attr("fill", d => colourScale(d, maxData))
    
    .transition()
    .duration(800)
    .ease(d3.easeCubicOut)
    .attr("y", d => h - (d / maxData * h))
    .attr("height", d => (d / maxData) * h);

// Add vote values
svg.selectAll("text.value")
    .data(dataset)
    .enter()
    .append("text")
    .attr("class", "value")
    .text(d => d)
    .attr("x", (d, i) => i * barWidth + (barWidth - barPadding) / 2)
    .attr("y", h)
    .attr("font-family", "sans-serif")
    .attr("fill", d => d === 0 ? "black" : "white")
    .attr("text-anchor", "middle")
    .attr("y", d => {
        const barHeight = (d / maxData) * h;
        return barHeight < 0.25 * h
            ? h - barHeight - 5
            : h - barHeight + 20;
    })
    .style("opacity", 0)  // Start hidden
    .transition()
    .duration(800)
    .delay(300) 
    .style("opacity", 1);  // Fade in

// Add labels below bars
svg.selectAll("text.label")
    .data(labels)
    .enter()
    .append("text")
    .attr("class", "label")
    .text(d => d)
    .attr("x", (d, i) => i * barWidth + (barWidth - barPadding) / 2)
    .attr("y", h + 20)
    .attr("font-family", "sans-serif")
    .attr("font-size", "12px")
    .attr("text-anchor", "middle");


    