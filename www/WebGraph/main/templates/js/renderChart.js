{% if lines %}

let chart = undefined;

$(document).ready(function () {
    if (chart !== undefined && chart != null) {
        chart.destroy();
    }

    const newWidth = Math.max({{lines | length}} * 20, 1000);
    document.getElementById("chart-container").style.width = newWidth + "px";


    // Création de 4 graphiques en fonction des directions
    const date = [];
    const occurrence = [];
    const top_left = [];
    const top_right = [];
    const bottom_left = [];
    const bottom_right = [];
    const classe = [];

    {% for line in lines %}
    date.push("{{line.0}}");
    occurrence.push({{ line.1}});
    top_left.push({{line.2}});
    top_right.push({{line.3}});
    bottom_left.push({{line.4}});
    bottom_right.push({{line.5}});
    classe.push("{{line.6}}");
    {% endfor %}

    // Création du graphique
    const ctx = document.getElementById('graphique').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: date,
            datasets: [{
                label: 'Top Left',
                data: top_left,
                fill: false,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)'
            }, {
                label: 'Top Right',
                data: top_right,
                fill: false,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)'
            }, {
                label: 'Bottom Left',
                data: bottom_left,
                fill: false,
                backgroundColor: 'rgba(255, 206, 86, 0.2)',
                borderColor: 'rgba(255, 206, 86, 1)'
            }, {
                label: 'Bottom Right',
                data: bottom_right,
                fill: false,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        stepSize: 1
                    }
                }]
            },
            tooltips: {
                callbacks: {
                    label: function (tooltipItem, data) {
                        let label = data.datasets[tooltipItem.datasetIndex].label || '';
                        if (label) label += ': ';
                        label += tooltipItem.yLabel;
                        return label;
                    }
                }
            }
        }
    });

    // Récupérer toutes les classes du CSV
    const class_names = Array.from(new Set(classe));

    // Mettre à jour le menu déroulant avec les options de classe
    let classSelect = document.getElementById('class-select');
    for (let i = 0; i < class_names.length; i++) {
        let option = document.createElement('option');
        option.text = class_names[i] + ' - ' + getName(class_names[i]);
        option.value = class_names[i];
        classSelect.appendChild(option);
    }

    // Gérer les changements de sélection dans le menu déroulant
    classSelect.addEventListener('change', function () {
        const selectedClass = classSelect.value;

        // Filtrer les données en fonction de la classe sélectionnée
        const filteredDate = [];
        const filteredOccurrence = [];
        const filteredTopLeft = [];
        const filteredTopRight = [];
        const filteredBottomLeft = [];
        const filteredBottomRight = [];

        for (let i = 0; i < classe.length; i++) {
            if (classe[i] === selectedClass) {
                filteredDate.push(date[i]);
                filteredOccurrence.push(occurrence[i]);
                filteredTopLeft.push(top_left[i]);
                filteredTopRight.push(top_right[i]);
                filteredBottomLeft.push(bottom_left[i]);
                filteredBottomRight.push(bottom_right[i]);
            }
        }

        // Mettre à jour le graphique avec les données filtrées
        chart.data.labels = filteredDate;
        chart.data.datasets[0].data = filteredTopLeft;
        chart.data.datasets[1].data = filteredTopRight;
        chart.data.datasets[2].data = filteredBottomLeft;
        chart.data.datasets[3].data = filteredBottomRight;
        chart.update();
    });

    // Définir les valeurs par défaut des champs de saisie de dates
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');

    startDateInput.addEventListener('change', function () {
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        updateChart(startDate, endDate);
        adjustCanvasWidth();
    });

    endDateInput.addEventListener('change', function () {
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        updateChart(startDate, endDate);
        adjustCanvasWidth();
    });

    function adjustCanvasWidth() {
        const newWidth = Math.max(chart.data.labels.length * 20, 1000);
        document.getElementById("chart-container").style.width = newWidth + "px";
    }

    function updateChart(startDate, endDate) {
        const filteredDate = [];
        const filteredOccurrence = [];
        const filteredTopLeft = [];
        const filteredTopRight = [];
        const filteredBottomLeft = [];
        const filteredBottomRight = [];

        for (let i = 0; i < date.length; i++) {
            if (isWithinRange(date[i], startDate, endDate)) {
                filteredDate.push(date[i]);
                filteredOccurrence.push(occurrence[i]);
                filteredTopLeft.push(top_left[i]);
                filteredTopRight.push(top_right[i]);
                filteredBottomLeft.push(bottom_left[i]);
                filteredBottomRight.push(bottom_right[i]);
            }
        }

        chart.data.labels = filteredDate;
        chart.data.datasets[0].data = filteredTopLeft;
        chart.data.datasets[1].data = filteredTopRight;
        chart.data.datasets[2].data = filteredBottomLeft;
        chart.data.datasets[3].data = filteredBottomRight;
        chart.update();
    }
});
{%endif %}