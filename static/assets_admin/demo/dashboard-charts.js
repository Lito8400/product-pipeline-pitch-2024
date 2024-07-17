// Rank chart
const colorstop1 = 'rgba(143, 162, 162, 1)';
const colorstop2 = 'rgba(143, 162, 162, 0)';
const colorborder = 'rgba(143, 162, 162, 1)';
const colorfont = 'rgb(173, 187, 199)';

function createChart(ctx, datalabel, datavalues, maxValue) {
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: datalabel,
            datasets: [{
              backgroundColor: function(context){
                const chart = context.chart;
                const { ctx, chartArea } = chart;

                var gradient = ctx.createLinearGradient(0, 0, 0, 188);
                gradient.addColorStop(0, colorstop1);
                gradient.addColorStop(1, colorstop2);

                if (!chartArea){
                  return gradient;
                }
                
                gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
                gradient.addColorStop(0, colorstop1);
                gradient.addColorStop(1, colorstop2);

                return gradient;
              },
              strokeColor : "#ff6c23",
              pointColor : "#fff",
              pointStrokeColor : "#ff6c23",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "#ff6c23",
              borderColor: colorborder,
              data: datavalues,
              borderWidth: 1
            }],
        },
        options: {
            scales: {
              xAxes: [{
                gridLines: {
                  display: false
                },
                ticks: {
                  fontColor: colorfont,
                  fontFamily: 'Aptos',
                }
              }],
              
              yAxes: [{
                ticks: {
                  min: 0,
                  max: maxValue,
                  fontColor: colorfont,
                  fontFamily: 'Aptos',
                },
                gridLines: {
                  display: true
                },
              }],
            },
            legend: {
              display: false,
              labels: {
                fontColor: colorfont 
              }
            },
            tooltips: {
              enabled: false
            },
            "defaultFontColor": colorfont,
            "animation": {
              "duration": 1,
              "onComplete": function() {
                var chartInstance = this.chart
                ctx = chartInstance.ctx;
                ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, 'Aptos');
                ctx.fillStyle = this.chart.config.options.defaultFontColor;
                ctx.textAlign = 'left';
                ctx.textBaseline = 'bottom';

                this.data.datasets.forEach(function(dataset, i) {
                  var meta = chartInstance.controller.getDatasetMeta(i);
                  meta.data.forEach(function(bar, index) {
                        var data = dataset.data[index];
                        ctx.fillText(data, bar._model.x - 5, bar._model.y - 5);
                  });
                });
              }
            },
        }
    });
};

fetch('/admin/dashboard-charts').then(response => response.json()).then(data => {
    // Rank Chart
    var canvases = document.querySelectorAll(".RankChart");
    canvases.forEach(canvas => {
        var ctx = canvas.getContext("2d");
        createChart(ctx, data.rankchartlabels, data.rankchartvalues, 6)
    });

    //Weighted Rank Chart
    canvases = document.querySelectorAll(".WeightedRankChart");
    canvases.forEach(canvas => {
        var ctx = canvas.getContext("2d");
        createChart(ctx, data.weightedrankchartlabels, data.weightedrankchartvalues, 6)
    });

    //Participation Chart
    canvases = document.querySelectorAll(".ParticipationChart");
    canvases.forEach(canvas => {
        var ctx = canvas.getContext("2d");
        let maxValue = Math.max(...data.participationchartvalues);
        let stepSize;

        // Xác định stepSize dựa trên maxValue
        if (maxValue < 10) {
            stepSize = 1;
        } else if (maxValue >= 10 && maxValue < 20) {
            stepSize = 2;
        } else if (maxValue >= 20 && maxValue < 50) {
            stepSize = 5;
        } else if (maxValue >= 50 && maxValue < 100) {
            stepSize = 10;
        } else if (maxValue >= 100 && maxValue < 200) {
            stepSize = 20;
        } else {
            stepSize = 50;
        }

        maxValue = Math.ceil(maxValue / stepSize) * stepSize + stepSize;
        createChart(ctx, data.participationchartlabels, data.participationchartvalues, maxValue)
    });

    //Interested Lanched Chart
    canvases = document.querySelectorAll(".InterestedLanchedChart");
    canvases.forEach(canvas => {
        var ctx = canvas.getContext("2d");
        createChart(ctx, data.interestedchartlabels, data.interestedchartvalues, 6)
    });

    //Path Market Chart
    canvases = document.querySelectorAll(".PathMarketChart");
    canvases.forEach(canvas => {
        var ctx = canvas.getContext("2d");
        createChart(ctx, data.marketchartlabels, data.marketchartvalues, 6)
    });

    //Pull Chart
    canvases = document.querySelectorAll(".PullSalesChart");
    canvases.forEach(canvas => {
        var ctx = canvas.getContext("2d");
        createChart(ctx, data.pullchartlabels, data.pullchartvalues, 6)
    });
});

var socket = io();

socket.on('update_dashboard_charts', function() {
    fetch('/admin/dashboard-charts').then(response => response.json()).then(data => {
        // Rank Chart
        var canvases = document.querySelectorAll(".RankChart");
        canvases.forEach(canvas => {
            var ctx = canvas.getContext("2d");
            createChart(ctx, data.rankchartlabels, data.rankchartvalues, 6)
        });
    
        //Weighted Rank Chart
        canvases = document.querySelectorAll(".WeightedRankChart");
        canvases.forEach(canvas => {
            var ctx = canvas.getContext("2d");
            createChart(ctx, data.weightedrankchartlabels, data.weightedrankchartvalues, 6)
        });
    
        //Participation Chart
        canvases = document.querySelectorAll(".ParticipationChart");
        canvases.forEach(canvas => {
            var ctx = canvas.getContext("2d");
            let maxValue = Math.max(...data.participationchartvalues);
            let stepSize;
    
            // Xác định stepSize dựa trên maxValue
            if (maxValue < 10) {
                stepSize = 1;
            } else if (maxValue >= 10 && maxValue < 20) {
                stepSize = 2;
            } else if (maxValue >= 20 && maxValue < 50) {
                stepSize = 5;
            } else if (maxValue >= 50 && maxValue < 100) {
                stepSize = 10;
            } else if (maxValue >= 100 && maxValue < 200) {
                stepSize = 20;
            } else {
                stepSize = 50;
            }

            maxValue = Math.ceil(maxValue / stepSize) * stepSize + stepSize;
            createChart(ctx, data.participationchartlabels, data.participationchartvalues, maxValue)
        });
    
        //Interested Lanched Chart
        canvases = document.querySelectorAll(".InterestedLanchedChart");
        canvases.forEach(canvas => {
            var ctx = canvas.getContext("2d");
            createChart(ctx, data.interestedchartlabels, data.interestedchartvalues, 6)
        });
    
        //Path Market Chart
        canvases = document.querySelectorAll(".PathMarketChart");
        canvases.forEach(canvas => {
            var ctx = canvas.getContext("2d");
            createChart(ctx, data.marketchartlabels, data.marketchartvalues, 6)
        });
    
        //Pull Chart
        canvases = document.querySelectorAll(".PullSalesChart");
        canvases.forEach(canvas => {
            var ctx = canvas.getContext("2d");
            createChart(ctx, data.pullchartlabels, data.pullchartvalues, 6)
        });
    });
});