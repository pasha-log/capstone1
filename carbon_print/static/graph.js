const CHART = document.getElementById('lineChart');
const BASE_URL = 'http://127.0.0.1:5000';

async function getData() {
	fetch(`${BASE_URL}/user/data`, { method: 'GET', method: 'POST' })
		.then((res) => res.json())
		.then((data) => {
			console.log(data);
			const chartData = {
				labels: data["Dates"],
				datasets: [
					{
						label: 'Vehicle Emissions',
						data: data['Carbon'],
						fill: false,
						borderColor: 'rgb(251, 141, 38, 1)',
						tension: 0.1,
						borderDash: [],
						borderCapStyle: 'butt',
						borderDashOffset: 0.0,
						borderJointStyle: 'miter',
						pointBorderColor: 'rgb(251, 141, 38, 1)',
						pointBackgroundColor: '#fff',
						pointBorderWidth: 1,
						pointHoverRadius: 5,
						pointHoverBackgroundColor: 'rgb(251, 141, 38, 1)',
						pointHoverBorderColor: 'rgba(220, 220, 220, 1)',
						pointHoverBorderWidth: 2,
						pointRadius: 1,
						pointHitRadius: 10,
						backgroundColor: 'rgba(255, 255, 255, 1)',
					}
				]
			};
			let lineChart = new Chart(CHART, {
				type: 'line',
				data: chartData,
                options: {
                    scales: {
                        y: {
                            title: {
                                display: true,
                                align: "center",
                                text: "Carbon(kg)",
                                color: 'rgba(0, 0, 0, 1)', 
                                font: {
                                    size: 12
                                },
                                padding: 4,

                            }
                        },
                        x: {
                            title: {
                                display: true,
                                align: "center",
                                text: "Timestamps",
                                color: 'rgba(0, 0, 0, 1)', 
                                font: {
                                    size: 12
                                },
                                padding: 4,

                            }
                        }
                    }
                }
			});
		})
		.catch((e) => console.log(e));
}

getData();
