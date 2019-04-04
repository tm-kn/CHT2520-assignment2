import Highcharts from 'highcharts';


export default function() {
    const chartContainer = document.querySelector('#js-per-project-chart');
    if (chartContainer) {
        Highcharts.chart(chartContainer, {
            chart: {
                type: 'column',
            },
            title: {
                text: 'Projects per week'
            },
            xAxis: {
                categories: [
                    'Monday',
                    'Tuesday',
                    'Wednesday'
                ],
            },

            series: [{
                name: 'RCA',
                data: [1, 2, 3],
            }, {
                name: 'CCA',
                data: [1, 2, 3],
            }]

        });
    }
}
