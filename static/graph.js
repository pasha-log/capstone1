const CHART = document.getElementById("lineChart");
const BASE_URL = "http://127.0.0.1:5000"
console.log(CHART);


let yAxis = [65, 59, 80, 81, 56, 55, 40]
let xAxis = ['January', 'February', 'March', 'April', 'May', 'June', 'July']

const data = {
    labels: xAxis,
    datasets: [{
        label: 'Vehicle Emissions',
        data: yAxis,
        fill: false,
        borderColor: 'rgb(251, 141, 38, 1)',
        tension: 0.1,
        borderDash: [],
        borderCapStyle: "butt",
        borderDashOffset: 0.0,
        borderJointStyle: "miter",
        pointBorderColor: "rgb(251, 141, 38, 1)",
        pointBackgroundColor: '#fff',
        pointBorderWidth: 1, 
        pointHoverRadius: 5,
        pointHoverBackgroundColor: "rgb(251, 141, 38, 1)", 
        pointHoverBorderColor: "rgba(220, 220, 220, 1)", 
        pointHoverBorderWidth: 2, 
        pointRadius: 1, 
        pointHitRadius: 10, 
        backgroundColor: "rgba(255, 255, 255, 1)",
    }]
};

let lineChart = new Chart(CHART, {
    type: 'line',
    data: data,
})

// $(document).ready(function(){
//     $(".chart a").click(async function () {
       
//         await fetch(`${BASE_URL}/user/chart`, {method: 'GET', method: 'POST'}).then((res) => 
//         res.json()).then((data) => {
//             console.log(data['Carbon'])
//         }).fetch(`${BASE_URL}/user/show`).catch((e) => alert('Could not show chart.'));
//       });
// })