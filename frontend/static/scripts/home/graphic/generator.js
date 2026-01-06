function rolling(data, wind) {
    let result = [];

    for (let i = 0; i < data.length; i++) {
        if (i < wind - 1) {
            result.push(null); 
        } else {
            let add = 0;
            for (let j = 0; j < wind; j++) {
                add += data[i - j];
            }
            result.push(add / wind);
        }
    }

    return result;
}


function serieTitlePublic(container,dt, price,medianMove, tx){

    let datasets = [
        {
            label: 'Preço Título',
            data: price,
            borderWidth:1,
            pointRadius: 0,
            backgroundColor: '#0F4D0F',
            borderColor: '#0F4D0F',
            pointHoverBackgroundColor: '#CCFFCC',
            pointHoverBorderColor: '#5CE65C',
            yAxisID: 'y'
        },
        {
            label: 'Media Movel',
            data: medianMove,
            borderWidth:1,
            pointRadius:0,
            backgroundColor:'#573000',
            borderColor: '#573000',
            pointHoverBackgroundColor: '#CCFFCC',
            pointHoverBorderColor: '#FF6600',

        },
        {
            label: 'Taxa (%)',
            data: tx,
            borderWidth:1,
            pointRadius: 0,
            yAxisID: 'y1',
            backgroundColor: '#f2f2f25b',
            borderColor: '#ff66005b',
            pointHoverBackgroundColor: '#CCFFCC',
            pointHoverBorderColor: '#FF6600',
            fill: true,
            tension: 0.6
        }     
    ]
    let labels = dt;
    let configAxisX = {
                    ticks: {
                        maxTicksLimit: 15,
                        maxRotation: 30,
                        minRotation: 40
                    },
                    grid: {               
                        display:false
                    }
                };
    
    let configPrimaryAxisY = {
                    type: 'linear',
                    display: true,
                    min: Math.min(...price)*0.95,
                    max:Math.max(...price)*1.01,
                    position: 'left',
                    ticks: {
                        font: {
                        size: 10, 
                        family: 'Arial',
                        },
                        callback: function(value) {
                        return 'R$ ' + parseInt(value); 
                        }
                    },
                    grid : {
                        display:true
                    },
                    title: {
                        display: false,
                    }
                }

    let configSecondAxisY = {
                    type: 'linear',
                    min: Math.min(...tx)*0.95,
                    max:Math.max(...tx)*1.01,
                    display: true,
                    position: 'right',
                    ticks: {
                        font: {
                        size: 10, 
                        family: 'Arial',
                        },
                        callback: function(value) {
                        return parseFloat(value).toFixed(2) + ' %'; 
                        }
                    },
                    grid: {
                        drawOnChartArea: false,
                        display:false 
                    },
                    title: {
                        display: true,
                        text: 'Taxa'
                    }
            }
    

    let lastPrice = price?.[price.length - 1];

    title = lastPrice
        ? Number(lastPrice).toFixed(2)
        : "0.00";
    let graphLine = new Chart(container, {
        type: 'line',
        data: {
        labels: labels,
        datasets: datasets
        },
        options: {
            scales: {
                x: configAxisX,
                y: configPrimaryAxisY,
                y1: configSecondAxisY
            },
            animation: false,
            plugins: {
                title:{
                    display: true,
                    text: `R$ ${title}`,
                    font: {
                        size: 16
                    },
                    align: 'start'
                },
                subtitle:{
                    display: true,
                    text: 'Fonte: Tesouro Direto',
                    align: 'start'
                },
                legend: {
                    display: true,
                    labels : {
                        usePointStyle: true,
                        pointStyle: 'line'
                    }           
                },
                zoom: {
                    zoom: {
                        wheel: {         
                            enabled: false
                        },
                        pinch: {          
                            enabled: true
                        },
                        mode: 'x',
                        drag: {
                        enabled: true,
                        backgroundColor: 'rgba(255, 0, 0, 0.2)',
                        borderWidth: 2,
                        borderColor: 'red'
                    }         
                    }
                }
            }
        }
    });
    return graphLine;
}