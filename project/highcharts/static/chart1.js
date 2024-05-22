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
    loadTeamData('BOS', '2001');
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
            createChart(nbaData)
        })
    fetch('physical_data/')
        .then(response => response.json())
        .then(loadedJson => {
            physicalData = loadedJson;
            createScatterChart(physicalData)
        })
});

function createScatterChart(data) {
    console.log("scatter data", data.map(obj => [obj.x, obj.y]));
    const options = {
        chart: {
            type: 'scatter',
            zoomType: 'xy'
        },
        title: {
            text: 'NBA athletes by height and weight',
            align: 'left'
        },
        xAxis: {
            title: {
                text: 'Height'
            },
            labels: {
                format: '{value} inch'
            },
            showLastLabel: true,
            min: 60
        },
        yAxis: {
            title: {
                text: 'Weight'
            },
            labels: {
                format: '{value} pound'
            },
            min: 100,
        },
        legend: {
            enabled: true
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 2.5,
                    symbol: 'circle',
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                jitter: {
                    x: 0.005
                }
            }
        },
        tooltip: {
            pointFormat: 'Height: {point.x} m <br/> Weight: {point.y} kg'
        },
        series: [{
            data: data.map(obj => [obj.x, obj.y])
        }]
    }
    const chart = Highcharts.chart('scatter-example', options);
}

function loadChart() {
    const selectTeam = document.getElementById("team");
    const selectYear = document.getElementById("year");
    const team = selectTeam.value; 
    const year = selectYear.value;
    console.log(team, year); 
    loadTeamData(team, year);
}

function loadTeamData(team, season) {
    fetch(`/team_data/${team}/${season}`)
        .then(response => response.json())
        .then(loadedJson => {
            teamData = loadedJson;
            console.log("team data received", teamData);
            createMainChart(teamData, team, season)
        })
}

function teamSelected() {
    console.log("team changed")
}
function createMainChart(teamData, team, season) {
    teamData.forEach(row => {
        row.MPG = Number.parseFloat(row.MPG);
        row.Age = Number.parseInt(row.Age)
    });
    teamData.sort((row1, row2) => row2.MPG - row1.MPG);
    const options = {
        chart: {
            type: 'bar',
        },
        title: {
            text: 'Minutes per game'
        },
        subtitle: {
            text: `${team} - ${season}` 
        },
        xAxis: {
            categories: teamData.map(row => row.Player)
        },
        yAxis: {
            title: {
                text: 'MPG'
            }
        },
        series: [{
            name: 'MPG',
            data: teamData.map(row => row.MPG)
        },
        {
            name: 'Age',
            data: teamData.map(row => row.Age)
        }       
        ],
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                }
            }
        }    
    }   
    const chart = Highcharts.chart('main-chart', options); 
    console.log("chart created");
}

function createChart(nbaData) {
    console.log("now", nbaData);
    nbaData.forEach(row => {
        row.MPG = Number.parseFloat(row.MPG);
        row.Age = Number.parseInt(row.Age)
    });
    nbaData.sort((row1, row2) => row2.MPG - row1.MPG);
    const options = {
        chart: {
            type: 'bar',
        },
        title: {
            text: 'Minutes per game'
        },
        subtitle: {
            text: "Boston Celtics - 1980"
        },
        xAxis: {
            categories: nbaData.map(row => row.Player)
        },
        yAxis: {
            title: {
                text: 'MPG'
            }
        },
        series: [{
            name: 'MPG',
            data: nbaData.map(row => row.MPG)
        },
        {
            name: 'Age',
            data: nbaData.map(row => row.Age)
        }       
        ],
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                }
            }
        }    
    }   
    const chart = Highcharts.chart('chart3', options); 
    console.log("chart created");
}