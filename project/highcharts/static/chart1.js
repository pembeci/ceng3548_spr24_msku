const options = {
    chart: {
        type: 'bar',
    },
    title: {
        text: 'Fruit Consumption'
    },
    subtitle: {
        text: "Example chart"
    },
    xAxis: {
        categories: ['Apples', 'Bananas', 'Oranges', 'Kiwi']
    },
    yAxis: {
        title: {
            text: 'Fruit eaten'
        }
    },
    series: [{
        name: 'Jane',
        data: [1, 0, 4, 1]
    }, {
        name: 'John',
        data: [5, 7, 3, 10]
    }, 
    {
        name: 'Izzet',
        data: [2, {y: 12, color: 'black', marker: { fillColor: '#BF0B23', radius: 14 }}, 7, 2]
    },        
    ],
    plotOptions: {
        line: {
            dataLabels: {
                enabled: true
            }
        }
    }    
}

document.addEventListener('DOMContentLoaded', function () {
    Highcharts.setOptions(
        {
        chart: {
            backgroundColor: {
                linearGradient: [0, 0, 500, 500],
                stops: [
                    [0, 'rgb(255, 255, 255)'],
                    [1, 'rgb(240, 240, 255)']
                ]
            },
            borderWidth: 5,
            borderColor: "pink",
            borderRadius: 10,
            plotBackgroundColor: 'rgba(255, 255, 255, .9)',
            plotShadow: true,
            plotBorderWidth: 1
        }
    }
    );
    const chart1 = Highcharts.chart('chart1', options);
    options.chart.type = "line";
    options.chart.zooming = {type: 'x'};
    const chart2 = Highcharts.chart('chart2', options);
    let nbaData = null; 
    fetch('static/bos_1980.json')
        .then(response => response.json())
        .then(loadedJson => {
            nbaData = loadedJson;
            console.log("now", nbaData);
        })
});