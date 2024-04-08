// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Bar Chart Example
fetch('/admin/participation-chart')
    .then(response => response.json())
    .then(data => {
        var ctx = document.getElementById("ParticipationChart");
        var myLineChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: [{
              backgroundColor: "rgba(2,117,216,1)",
              borderColor: "rgba(2,117,216,1)",
              data: data.values,
            }],
          },
          options: {
            scales: {
              xAxes: [{
                gridLines: {
                  display: false
                },
                ticks: {
                  maxTicksLimit: 6
                }
              }],
              yAxes: [{
                ticks: {
                  min: 0,
                  maxTicksLimit: 6
                },
                gridLines: {
                  display: true
                }
              }],
              
            },
            legend: {
              display: false
            }
          }
        });
    });
