document.addEventListener('DOMContentLoaded', function () {
    const select = document.getElementById('csv-select');
    const chartContainer = document.getElementById('chart-container');
    let chart;

    // Function to load CSV file data
    function loadCSV(filename) {
        // Fetch the CSV file
        fetch(`static/captured_emotions_data/${filename}`)
            .then(response => response.text())
            .then(csvData => {
                // Parse CSV data
                const data = parseCSV(csvData);
                        // Get selected chart type
                const selectedChart = chartSelect.value;

                        // Plot chart based on selected CSV data and chart type
                switch (selectedChart) {
                    case 'doughnut':
                        createLineChart(data);
                        break;
                    case 'bar':
                        createBarChart(data);
                        break;
                    case 'pie':
                        createPieChart(data);
                        break;
                }
            })
            .catch(error => console.error('Error fetching CSV file:', error));
    }

    // Function to parse CSV data
    function parseCSV(csvData) {
        const rows = csvData.split('\n').map(row => row.split(','));
        const labels = [];
        const durations = [];

        // Start from index 1 to skip the header row
        for (let i = 1; i < rows.length; i++) {
            const row = rows[i];
            if (row.length >= 5) {
                labels.push(row[2]); // Emotion
                durations.push(parseFloat(row[3])); // Duration
            }
        }

        return {
            labels: labels,
            values: durations
        };
    }

    // Function to update chart with new data
    function createPieChart(data) {
        if (chart) {
            chart.destroy(); // Destroy previous chart instance
        }

        // Initialize an object to store unique labels and their summed values
        const uniqueData = {};
        
        // Iterate through the data.labels array
        data.labels.forEach((label, index) => {
            // If the label is already in uniqueData, add the current value to its sum
            if (label in uniqueData) {
                uniqueData[label] += data.values[index];
            } 
            // If the label is not in uniqueData, initialize its sum with the current value
            else {
                uniqueData[label] = data.values[index];
            }
        });

        // Separate unique labels and values
        const uniqueLabels = Object.keys(uniqueData);
        const uniqueValues = Object.values(uniqueData);

        const customColors = [
            'rgba(255, 99, 132, 0.2)', // Example custom color 1
            'rgba(54, 162, 235, 0.2)', // Example custom color 2
            'rgba(255, 206, 86, 0.2)', // Example custom color 3
            'rgba(75, 192, 192, 0.2)', // Example custom color 4
            'rgba(153, 102, 255, 0.2)', // Example custom color 5
            'rgba(255, 159, 64, 0.2)', // Example custom color 6
            'rgba(0, 204, 102, 0.2)' // Example custom color 7
        ];        

        chart = new Chart('myChart', {
            type: 'pie',
            data: {
                labels: uniqueLabels,
                datasets: [{
                    label: 'Duration',
                    data: uniqueValues,
                    backgroundColor: customColors.slice(0, data.labels.length),
                    borderColor: 'rgba(25, 99, 132, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

        // Function to update chart with new data
        function createBarChart(data) {
            if (chart) {
                chart.destroy(); // Destroy previous chart instance
            }
    
            // Initialize an object to store unique labels and their summed values
            const uniqueData = {};
            
            // Iterate through the data.labels array
            data.labels.forEach((label, index) => {
                // If the label is already in uniqueData, add the current value to its sum
                if (label in uniqueData) {
                    uniqueData[label] += data.values[index];
                } 
                // If the label is not in uniqueData, initialize its sum with the current value
                else {
                    uniqueData[label] = data.values[index];
                }
            });
    
            // Separate unique labels and values
            const uniqueLabels = Object.keys(uniqueData);
            const uniqueValues = Object.values(uniqueData);
    
            const customColors = [
                'rgba(255, 99, 132, 0.2)', // Example custom color 1
                'rgba(54, 162, 235, 0.2)', // Example custom color 2
                'rgba(255, 206, 86, 0.2)', // Example custom color 3
                'rgba(75, 192, 192, 0.2)', // Example custom color 4
                'rgba(153, 102, 255, 0.2)', // Example custom color 5
                'rgba(255, 159, 64, 0.2)', // Example custom color 6
                'rgba(0, 204, 102, 0.2)' // Example custom color 7
            ];        
    
            chart = new Chart('myChart', {
                type: 'bar',
                data: {
                    labels: uniqueLabels,
                    datasets: [{
                        label: 'Duration',
                        data: uniqueValues,
                        backgroundColor: customColors.slice(0, data.labels.length),
                        borderColor: 'rgba(25, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

            // Function to update chart with new data
    function createLineChart(data) {
        if (chart) {
            chart.destroy(); // Destroy previous chart instance
        }

        // Initialize an object to store unique labels and their summed values
        const uniqueData = {};
        
        // Iterate through the data.labels array
        data.labels.forEach((label, index) => {
            // If the label is already in uniqueData, add the current value to its sum
            if (label in uniqueData) {
                uniqueData[label] += data.values[index];
            } 
            // If the label is not in uniqueData, initialize its sum with the current value
            else {
                uniqueData[label] = data.values[index];
            }
        });

        // Separate unique labels and values
        const uniqueLabels = Object.keys(uniqueData);
        const uniqueValues = Object.values(uniqueData);

        const customColors = [
            'rgba(255, 99, 132, 0.2)', // Example custom color 1
            'rgba(54, 162, 235, 0.2)', // Example custom color 2
            'rgba(255, 206, 86, 0.2)', // Example custom color 3
            'rgba(75, 192, 192, 0.2)', // Example custom color 4
            'rgba(153, 102, 255, 0.2)', // Example custom color 5
            'rgba(255, 159, 64, 0.2)', // Example custom color 6
            'rgba(0, 204, 102, 0.2)' // Example custom color 7
        ];        

        chart = new Chart('myChart', {
            type: 'doughnut',
            data: {
                labels: uniqueLabels,
                datasets: [{
                    label: 'Duration',
                    data: uniqueValues,
                    backgroundColor: customColors.slice(0, data.labels.length),
                    borderColor: 'rgba(25, 99, 132, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Event listener for dropdown change
    select.addEventListener('change', function () {
        const selectedFile = this.value;
        loadCSV(selectedFile);
    });

// Function to populate dropdown with CSV file options
function populateDropdown() {
    fetch('/csv-files')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(csvFiles => {
            // Clear existing options
            select.innerHTML = '';

            // Populate dropdown with new options
            csvFiles.forEach(filename => {
                const option = document.createElement('option');
                option.text = filename;
                option.value = filename;
                select.add(option);
            });
        })
        .catch(error => console.error('Error fetching or parsing CSV files:', error));
}


    // Call the function to populate dropdown initially
    populateDropdown();

});
