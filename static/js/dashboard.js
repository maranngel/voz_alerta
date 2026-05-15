// Chart Initialization
function initChart(stats) {
    const ctx = document.getElementById('signalsChart').getContext('2d');
    const signalsChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Verde', 'Amarillo', 'Rojo'],
            datasets: [{
                data: [stats.GREEN, stats.YELLOW, stats.RED],
                backgroundColor: ['#00ff88', '#ffcc00', '#ff3333'],
                borderColor: 'rgba(255,255,255,0.1)',
                borderWidth: 2,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#a0a0a0',
                        font: { family: 'Inter' }
                    }
                }
            },
            cutout: '70%'
        }
    });
    return signalsChart;
}

let selectedLevel = null;
let currentChart = null;
let statsData = null;

function openModal(level) {
    selectedLevel = level;
    const title = document.getElementById('modalTitle');
    const color = level === 'RED' ? '#ff3333' : (level === 'YELLOW' ? '#ffcc00' : '#00ff88');
    title.style.color = color;
    title.innerText = `ACTIVAR ${level} - DATOS DEL PACIENTE`;
    document.getElementById('patientModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('patientModal').style.display = 'none';
    document.getElementById('patientName').value = '';
    document.getElementById('patientAge').value = '';
    document.getElementById('modalDescription').value = '';
}

function confirmSignal(triggerUrl, csrfToken) {
    if (selectedLevel) {
        sendSignal(selectedLevel, triggerUrl, csrfToken);
        closeModal();
    }
}

function sendSignal(level, triggerUrl, csrfToken) {
    const patientName = document.getElementById('patientName').value;
    const patientAge = document.getElementById('patientAge').value;
    const description = document.getElementById('modalDescription').value;

    const formData = new FormData();
    formData.append('level', level);
    formData.append('description', description);
    formData.append('patient_name', patientName);
    formData.append('patient_age', patientAge);
    formData.append('csrfmiddlewaretoken', csrfToken);

    fetch(triggerUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showToast(`Señal ${level} Desplegada`);
            addSignalToList(data);
            announceSignal(level, description);
            updateChart(level);
            
            const body = document.body;
            const originalBg = body.style.backgroundColor;
            const flashColor = level === 'RED' ? '#220000' : (level === 'YELLOW' ? '#221100' : '#001100');
            body.style.backgroundColor = flashColor;
            setTimeout(() => body.style.backgroundColor = originalBg, 500);
        }
    });
}

function updateChart(level) {
    if (statsData && currentChart) {
        statsData[level]++;
        currentChart.data.datasets[0].data = [statsData.GREEN, statsData.YELLOW, statsData.RED];
        currentChart.update();
    }
}

function announceSignal(level, description) {
    if (!('speechSynthesis' in window)) return;
    
    const levelNames = {
        'GREEN': 'Código Verde, nivel bajo.',
        'YELLOW': 'Código Amarillo, nivel intermedio.',
        'RED': 'Código Rojo, nivel crítico.'
    };

    let text = `Atención. Se ha activado ${levelNames[level]}`;
    if (description) {
        text += ` Detalles: ${description}`;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'es-ES';
    utterance.rate = 0.9;
    utterance.pitch = 1;
    window.speechSynthesis.speak(utterance);
}

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.innerText = message;
    toast.style.display = 'block';
    setTimeout(() => toast.style.display = 'none', 3000);
}

function addSignalToList(data) {
    const list = document.getElementById('signalList');
    const item = document.createElement('li');
    item.className = 'signal-item';
    
    let label = data.level === 'GREEN' ? 'Código Verde - Bajo' : 
                (data.level === 'YELLOW' ? 'Código Amarillo - Intermedio' : 'Código Rojo - Alto');
    
    let patientHtml = data.patient_name ? `<span class="patient-info-tag">Paciente: ${data.patient_name}</span>` : '';
    let descriptionHtml = data.description ? `<span class="signal-description">${data.description}</span>` : '';

    item.innerHTML = `
        <div>
            <span class="level-tag tag-${data.level.toLowerCase()}">${label}</span>
            <span class="user-tag">por ${data.user}</span>
            ${patientHtml}
            ${descriptionHtml}
        </div>
        <span class="timestamp">${data.timestamp}</span>
    `;
    list.insertBefore(item, list.firstChild);
    
    if (list.children.length > 10) {
        list.removeChild(list.lastChild);
    }
}
