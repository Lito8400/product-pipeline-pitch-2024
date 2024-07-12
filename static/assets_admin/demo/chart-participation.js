// Set new default font family and font color to mimic Bootstrap's default styling
const p_colorstop1 = 'rgba(143, 162, 162, 1)';
const p_colorstop2 = 'rgba(143, 162, 162, 0)';
const p_colorborder = 'rgba(143, 162, 162, 1)';
const p_colorfont = 'rgb(173, 187, 199)';

// Bar Chart Example
fetch('/admin/participation-chart')
    .then(response => response.json())
    .then(data => {
        var canvases = document.querySelectorAll(".ParticipationChart");
        canvases.forEach(canvas => {
        var ctx = canvas.getContext("2d");
        let maxValue = parseInt(Math.max(...data.values)) + 1;
        var myLineChart_Participation = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: [{
              backgroundColor: function(context){
                const chart = context.chart;
                const { ctx, chartArea } = chart;

                var gradient = ctx.createLinearGradient(0, 0, 0, 188);
                // gradient.addColorStop(0, 'rgba(255, 140, 0, 1)');
                // gradient.addColorStop(1, 'rgba(255, 140, 0, 0)');
                // gradient.addColorStop(0, 'rgba(135, 206, 250, 1)');
                // gradient.addColorStop(1, 'rgba(135, 206, 250, 0)');

                gradient.addColorStop(0, p_colorstop1);
                gradient.addColorStop(1, p_colorstop2);

                if (!chartArea){
                  return gradient;
                }
                
                gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
                // gradient.addColorStop(0, 'rgba(255, 140, 0, 1)');
                // gradient.addColorStop(1, 'rgba(255, 140, 0, 0)');
                // gradient.addColorStop(0, 'rgba(135, 206, 250, 1)');
                // gradient.addColorStop(1, 'rgba(135, 206, 250, 0)');

                gradient.addColorStop(0, p_colorstop1);
                gradient.addColorStop(1, p_colorstop2);
                return gradient;
              },
              strokeColor : "#ff6c23",
              pointColor : "#fff",
              pointStrokeColor : "#ff6c23",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "#ff6c23",
              borderColor: p_colorborder,
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
                  fontColor: p_colorfont,
                  fontFamily: 'Aptos',
                }
              }],
              
              yAxes: [{
                ticks: {
                  min: 0,
                  max: maxValue,
                  fontColor: p_colorfont,
                  fontFamily: 'Aptos',
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
                fontColor: p_colorfont 
              }
            },
            "defaultFontColor": p_colorfont,
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
                        ctx.fillText(data, bar._model.x -2, bar._model.y - 5);
                  });
                });
              }
            },
          }
        });
      });
    });

    var socket = io();

    socket.on('update_participation_chart', function() {
      fetch('/admin/participation-chart')
      .then(response => response.json())
      .then(data => {
        var canvases = document.querySelectorAll(".ParticipationChart");
        canvases.forEach(canvas => {
        var ctx = canvas.getContext("2d");
        // if (window.myLineChart_Participation) {
        //   window.myLineChart_Participation.destroy();
        // }

        let maxValue = parseInt(Math.max(...data.values)) + 1;
        window.myLineChart_Participation = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: [{
              backgroundColor: function(context){
                const chart = context.chart;
                const { ctx, chartArea } = chart;

                var gradient = ctx.createLinearGradient(0, 0, 0, 188);
                gradient.addColorStop(0, p_colorstop1);
                gradient.addColorStop(1, p_colorstop2);

                if (!chartArea){
                  return gradient;
                }
                
                gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom - 50);
                gradient.addColorStop(0, p_colorstop1);
                gradient.addColorStop(1, p_colorstop2);
                return gradient;
              },
              strokeColor : "#ff6c23",
              pointColor : "#fff",
              pointStrokeColor : "#ff6c23",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "#ff6c23",
              borderColor: p_colorborder,
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
                  fontColor: p_colorfont,
                  fontFamily: 'Aptos',
                }
              }],
              
              yAxes: [{
                ticks: {
                  min: 0,
                  max: maxValue,
                  fontColor: p_colorfont,
                  fontFamily: 'Aptos',
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
                fontColor: p_colorfont 
              }
            },
            "defaultFontColor": p_colorfont,
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
                        ctx.fillText(data, bar._model.x -2, bar._model.y - 5);
                  });
                });
              }
            },
          }
        });
      });
    });
    });