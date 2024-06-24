// Set new default font family and font color to mimic Bootstrap's default styling


// Bar Chart Example
fetch('/admin/rank-chart')
    .then(response => response.json())
    .then(data => {
        var canvases = document.querySelectorAll(".RankChart");
        canvases.forEach(canvas => {
        var ctx = canvas.getContext("2d");
        var myLineChart_Rank = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: [{
              backgroundColor: function(context){
                const chart = context.chart;
                const { ctx, chartArea } = chart;

                var gradient = ctx.createLinearGradient(0, 0, 0, 188);
                gradient.addColorStop(0, 'rgba(135, 206, 250, 1)');
                gradient.addColorStop(1, 'rgba(135, 206, 250, 0)');

                if (!chartArea){
                  return gradient;
                }
                
                gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom -65);
                gradient.addColorStop(0, 'rgba(135, 206, 250, 1)');
                gradient.addColorStop(1, 'rgba(135, 206, 250, 0)');
                return gradient;
              },
              strokeColor : "#ff6c23",
              pointColor : "#fff",
              pointStrokeColor : "#ff6c23",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "#ff6c23",
              borderColor: "rgb(135, 206, 250)",
              data: data.values,
              borderWidth: 1
            }],
          },
          options: {
            scales: {
              xAxes: [{
                gridLines: {
                  // color: 'rgb(59,69,67)',
                  display: false
                },
                ticks: {
                  fontColor: 'rgb(221, 221, 221)' 
                }
              }],
              
              yAxes: [{
                ticks: {
                  min: 0,
                  max: 6,
                  fontColor: 'rgb(221, 221, 221)' 
                },
                gridLines: {
                  // color: 'rgb(59,69,67)',
                  display: true
                },
              }],
            },
            legend: {
              display: false,
              labels: {
                fontColor: 'rgb(221, 221, 221)' 
              }
            },
            "defaultFontColor": 'rgb(221, 221, 221)',
            "animation": {
              "duration": 1,
              "onComplete": function() {
                var chartInstance = this.chart
                ctx = chartInstance.ctx;
                ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
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
      })
    });

    var socket = io();

    socket.on('update_rank_chart', function() {
      fetch('/admin/rank-chart')
      .then(response => response.json())
      .then(data => {
        var canvases = document.querySelectorAll(".RankChart");
        canvases.forEach(canvas => {
        var ctx = canvas.getContext("2d");
        // if (window.myLineChart_Rank) {
        //   window.myLineChart_Rank.destroy();
        // }
        window.myLineChart_Rank = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: [{
              backgroundColor: function(context){
                const chart = context.chart;
                const { ctx, chartArea } = chart;

                var gradient = ctx.createLinearGradient(0, 0, 0, 188);
                gradient.addColorStop(0, 'rgba(135, 206, 250, 1)');
                gradient.addColorStop(1, 'rgba(135, 206, 250, 0)');

                if (!chartArea){
                  return gradient;
                }
                
                gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom -65);
                gradient.addColorStop(0, 'rgba(135, 206, 250, 1)');
                gradient.addColorStop(1, 'rgba(135, 206, 250, 0)');
                return gradient;
              },
              strokeColor : "#ff6c23",
              pointColor : "#fff",
              pointStrokeColor : "#ff6c23",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "#ff6c23",
              borderColor: "rgb(135, 206, 250)",
              data: data.values,
              borderWidth: 1
            }],
          },
          options: {
            scales: {
              xAxes: [{
                gridLines: {
                  // color: 'rgb(59,69,67)',
                  display: false
                },
                ticks: {
                  fontColor: 'rgb(221, 221, 221)' 
                }
              }],
              
              yAxes: [{
                ticks: {
                  min: 0,
                  max: 6,
                  fontColor: 'rgb(221, 221, 221)' 
                },
                gridLines: {
                  // color: 'rgb(59,69,67)',
                  display: true
                },
              }],
            },
            legend: {
              display: false,
              labels: {
                fontColor: 'rgb(221, 221, 221)' 
              }
            },
            "defaultFontColor": 'rgb(221, 221, 221)',
            "animation": {
              "duration": 1,
              "onComplete": function() {
                var chartInstance = this.chart
                ctx = chartInstance.ctx;
                ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
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
      })
    });
    });
