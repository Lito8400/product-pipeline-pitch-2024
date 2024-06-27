const w_colorstop1 = 'rgba(143, 162, 162, 1)';
const w_colorstop2 = 'rgba(143, 162, 162, 0)';
const w_colorborder = 'rgba(143, 162, 162, 1)';
const w_colorfont = 'rgb(173, 187, 199)';

// Bar Chart Example
fetch('/admin/weighted-rank-chart')
    .then(response => response.json())
    .then(data => {
        var canvases = document.querySelectorAll(".WeightedRankChart");
        canvases.forEach(canvas => {
        var ctx = canvas.getContext("2d");
        var myLineChart_Weighted = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: [{
              backgroundColor: function(context){
                const chart = context.chart;
                const { ctx, chartArea } = chart;

                var gradient = ctx.createLinearGradient(0, 0, 0, 188);
                // gradient.addColorStop(0, 'rgba(255, 165, 0, 1)');
                // gradient.addColorStop(1, 'rgba(255, 165, 0, 0)');
                // gradient.addColorStop(0, 'rgba(100, 149, 237, 1)');
                // gradient.addColorStop(1, 'rgba(100, 149, 237, 0)');
                
                gradient.addColorStop(0, w_colorstop1);
                gradient.addColorStop(1, w_colorstop2);

                if (!chartArea){
                  return gradient;
                }
                
                gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
                // gradient.addColorStop(0, 'rgba(255, 165, 0, 1)');
                // gradient.addColorStop(1, 'rgba(255, 165, 0, 0)');
                // gradient.addColorStop(0, 'rgba(100, 149, 237, 1)');
                // gradient.addColorStop(1, 'rgba(100, 149, 237, 0)');

                gradient.addColorStop(0, w_colorstop1);
                gradient.addColorStop(1, w_colorstop2);
                return gradient;
              },
              strokeColor : "#ff6c23",
              pointColor : "#fff",
              pointStrokeColor : "#ff6c23",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "#ff6c23",
              borderColor: w_colorborder,
              data: data.values,
              borderWidth: 1,
            }],
          },
          options: {
            scales: {
              xAxes: [{
                gridLines: {
                  // color: 'rgb(134, 145, 148)',
                  display: false
                },
                ticks: {
                  fontColor: w_colorfont
                }
              }],
              
              yAxes: [{
                ticks: {
                  min: 0,
                  max: 6,
                  fontColor: w_colorfont
                },
                gridLines: {
                  // color: 'rgb(134, 145, 148)',
                  display: true
                },
              }],
            },
            legend: {
              display: false,
              labels: {
                fontColor: w_colorfont
              }
            },
            "defaultFontColor": w_colorfont,
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
      });
    });

    var socket = io();

    socket.on('update_weighted_rank_chart', function() {
      fetch('/admin/weighted-rank-chart')
      .then(response => response.json())
      .then(data => {
        var canvases = document.querySelectorAll(".WeightedRankChart");
        canvases.forEach(canvas => {
        var ctx = canvas.getContext("2d");
        // if (window.myLineChart_Weighted) {
        //   window.myLineChart_Weighted.destroy();
        // }
        window.myLineChart_Weighted = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: [{
              backgroundColor: function(context){
                const chart = context.chart;
                const { ctx, chartArea } = chart;

                var gradient = ctx.createLinearGradient(0, 0, 0, 188);
                gradient.addColorStop(0, w_colorstop1);
                gradient.addColorStop(1, w_colorstop2);

                if (!chartArea){
                  return gradient;
                }
                
                gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom - 65);
                gradient.addColorStop(0, w_colorstop1);
                gradient.addColorStop(1, w_colorstop2);
                return gradient;
              },
              strokeColor : "#ff6c23",
              pointColor : "#fff",
              pointStrokeColor : "#ff6c23",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "#ff6c23",
              borderColor: w_colorborder,
              data: data.values,
              borderWidth: 1
            }],
          },
          options: {
            scales: {
              xAxes: [{
                gridLines: {
                  // color: 'rgb(134, 145, 148)',
                  display: false
                },
                ticks: {
                  fontColor: w_colorfont
                }
              }],
              
              yAxes: [{
                ticks: {
                  min: 0,
                  max: 6,
                  fontColor: w_colorfont
                },
                gridLines: {
                  // color: 'rgb(134, 145, 148)',
                  display: true
                },
              }],
            },
            legend: {
              display: false,
              labels: {
                fontColor: w_colorfont
              }
            },
            "defaultFontColor": w_colorfont,
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
      });
    });

    });
