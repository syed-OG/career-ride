document.addEventListener('DOMContentLoaded', function() {
    // Progress Chart (Dashboard)
    const progressCtx = document.getElementById('progressChart');
    if (progressCtx) {
        const progressLabels = progressCtx.dataset.labels ? JSON.parse(progressCtx.dataset.labels) : [];
        const progressData = progressCtx.dataset.values ? JSON.parse(progressCtx.dataset.values) : [];
        
        new Chart(progressCtx, {
            type: 'line',
            data: {
                labels: progressLabels,
                datasets: [{
                    label: 'Academic Progress',
                    data: progressData,
                    backgroundColor: 'rgba(111, 66, 193, 0.2)',
                    borderColor: '#6f42c1',
                    borderWidth: 2,
                    pointBackgroundColor: '#6f42c1',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#6f42c1',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Completion (%)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Time Period'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                }
            }
        });
    }

    // Career Match Chart (Career Paths)
    const matchCharts = document.querySelectorAll('.career-match-chart');
    if (matchCharts) {
        matchCharts.forEach(function(chartElement) {
            const score = parseInt(chartElement.dataset.score) || 0;
            
            new Chart(chartElement, {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: [score, 100 - score],
                        backgroundColor: ['#6f42c1', '#e9ecef'],
                        borderWidth: 0
                    }]
                },
                options: {
                    cutout: '70%',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            enabled: false
                        }
                    }
                }
            });
            
            // Add center text
            const parent = chartElement.parentElement;
            const scoreText = document.createElement('div');
            scoreText.className = 'chart-center-text';
            scoreText.textContent = `${score}%`;
            parent.style.position = 'relative';
            scoreText.style.position = 'absolute';
            scoreText.style.top = '50%';
            scoreText.style.left = '50%';
            scoreText.style.transform = 'translate(-50%, -50%)';
            scoreText.style.fontSize = '1.5rem';
            scoreText.style.fontWeight = 'bold';
            scoreText.style.color = '#6f42c1';
            parent.appendChild(scoreText);
        });
    }

    // Aptitude Test Results Chart
    const aptitudeChartCtx = document.getElementById('aptitudeResultsChart');
    if (aptitudeChartCtx) {
        const categories = aptitudeChartCtx.dataset.categories ? JSON.parse(aptitudeChartCtx.dataset.categories) : [];
        const scores = aptitudeChartCtx.dataset.scores ? JSON.parse(aptitudeChartCtx.dataset.scores) : [];
        const maxScores = aptitudeChartCtx.dataset.maxScores ? JSON.parse(aptitudeChartCtx.dataset.maxScores) : [];
        
        new Chart(aptitudeChartCtx, {
            type: 'bar',
            data: {
                labels: categories,
                datasets: [
                    {
                        label: 'Your Score',
                        data: scores,
                        backgroundColor: '#6f42c1',
                        barPercentage: 0.6
                    },
                    {
                        label: 'Maximum Score',
                        data: maxScores,
                        backgroundColor: '#e9ecef',
                        barPercentage: 0.6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Score'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Test Categories'
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                }
            }
        });
    }

    // Skills Radar Chart (Profile)
    const skillsChartCtx = document.getElementById('skillsRadarChart');
    if (skillsChartCtx) {
        const skills = skillsChartCtx.dataset.skills ? JSON.parse(skillsChartCtx.dataset.skills) : [];
        const levels = skillsChartCtx.dataset.levels ? JSON.parse(skillsChartCtx.dataset.levels) : [];
        
        new Chart(skillsChartCtx, {
            type: 'radar',
            data: {
                labels: skills,
                datasets: [{
                    label: 'Skill Level',
                    data: levels,
                    backgroundColor: 'rgba(111, 66, 193, 0.2)',
                    borderColor: '#6f42c1',
                    pointBackgroundColor: '#6f42c1',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#6f42c1'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: {
                            display: true
                        },
                        suggestedMin: 0,
                        suggestedMax: 5
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    // Course Completion Chart (Dashboard)
    const courseCompletionCtx = document.getElementById('courseCompletionChart');
    if (courseCompletionCtx) {
        const completed = parseInt(courseCompletionCtx.dataset.completed) || 0;
        const inProgress = parseInt(courseCompletionCtx.dataset.inProgress) || 0;
        const planned = parseInt(courseCompletionCtx.dataset.planned) || 0;
        
        new Chart(courseCompletionCtx, {
            type: 'pie',
            data: {
                labels: ['Completed', 'In Progress', 'Planned'],
                datasets: [{
                    data: [completed, inProgress, planned],
                    backgroundColor: ['#28a745', '#ffc107', '#e9ecef'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
});
