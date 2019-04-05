import Highcharts from 'highcharts';
import moment from 'moment';


async function getData(apiURL) {
    const response = await fetch(apiURL, {
        headers: {
            'Accept': 'application/json',
        },
        mode: 'same-origin',
    });
    return response.json();
}

function getDurationFromMinutes(rawMinutes) {
    const hours = Math.floor(rawMinutes / 60);
    const minutes = Math.floor(rawMinutes % 60);
    return `${hours}h ${minutes}min.`;
}

function setupChart(container, data) {
    const projects = [];

    Highcharts.chart(container, {
        chart: {
            type: 'column',
        },

        title: {
            text: null,
        },

        xAxis: {
            categories: data.days,
            labels: {
                formatter: function() {
                    return moment(this.value).format('ddd Do MMM YYYY')
                },
            }
        },

        yAxis: {
            labels: {
                formatter: function() {
                    return getDurationFromMinutes(this.value);
                },
            }
        },

        tooltip: {
            pointFormatter: function() {
                return `${getDurationFromMinutes(this.y)}`
            },
        },

        series: data.projects.map(v => ({
            name: v.title,
            data: v.days.map(v => v.duration_seconds/60),
        })),
    });
}

export default async function() {
    const chartContainer = document.querySelector('#js-per-project-chart');
    if (chartContainer) {
        const data = await getData(chartContainer.dataset.apiUrl);
        setupChart(chartContainer, data);
    }
}
