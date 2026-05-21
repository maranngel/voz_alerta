/*
 * dashboard.js
 * Controla la lógica principal del panel de mando (Dashboard) en el lado del cliente (Frontend).
 * Se encarga de gestionar el envío de señales por AJAX,
 * la actualización de la gráfica interactiva en tiempo real y las notificaciones.
 */

// Función para inicializar el gráfico de pastel (Doughnut) usando la librería Chart.js
// Recibe un objeto 'stats' con el conteo actual de cada tipo de señal
function initChart(stats) {
    // Obtenemos el contexto 2D del elemento canvas HTML donde se dibujará la gráfica
    const ctx = document.getElementById('signalsChart').getContext('2d');
    
    // Instanciamos el gráfico pasándole el contexto y la configuración
    const signalsChart = new Chart(ctx, {
        type: 'doughnut', // Tipo de gráfico: rosquilla o doughnut
        data: {
            // Etiquetas correspondientes a las porciones del gráfico
            labels: ['Verde', 'Amarillo', 'Rojo'],
            datasets: [{
                // Los datos provienen del objeto stats inyectado desde Django (Backend)
                data: [stats.GREEN, stats.YELLOW, stats.RED],
                // Colores para cada porción del gráfico
                backgroundColor: ['#00ff88', '#ffcc00', '#ff3333'],
                // Borde suave entre las porciones
                borderColor: 'rgba(255,255,255,0.1)',
                borderWidth: 2,
                // Efecto de desplazamiento al pasar el ratón
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true, // Se adapta al tamaño del contenedor
            plugins: {
                legend: {
                    position: 'bottom', // Leyenda en la parte inferior
                    labels: {
                        color: '#a0a0a0',
                        font: { family: 'Inter' }
                    }
                }
            },
            cutout: '70%' // Grosor de la rosquilla (70% vacío en el centro)
        }
    });
    // Retornamos la instancia para poder actualizarla más adelante sin recargar la página
    return signalsChart;
}

// ========================================================
// VARIABLES GLOBALES
// Estas variables mantienen el estado de la aplicación en la vista
// ========================================================
let selectedLevel = null;   // Almacena el nivel de alerta que el usuario va a disparar ('GREEN', 'YELLOW', 'RED')
let currentChart = null;    // Guarda la instancia del gráfico Chart.js
let statsData = null;       // Guarda los datos estadísticos actuales

// Abre el modal (ventana emergente) de confirmación de señal y ajusta su título según el nivel.
function openModal(level) {
    selectedLevel = level; // Guardamos el nivel seleccionado
    const title = document.getElementById('modalTitle'); // Seleccionamos el título del modal
    
    // Determinamos el color adecuado según la alerta elegida
    const color = level === 'RED' ? '#ff3333' : (level === 'YELLOW' ? '#ffcc00' : '#00ff88');
    title.style.color = color;
    
    // Actualizamos el texto del título dinámicamente
    title.innerText = `ACTIVAR ${level} - DATOS DEL PACIENTE`;
    
    // Mostramos el modal cambiando su estilo 'display'
    document.getElementById('patientModal').style.display = 'flex';
}

// Cierra el modal y limpia los campos del formulario para que esté vacío la próxima vez
function closeModal() {
    // Ocultamos el modal
    document.getElementById('patientModal').style.display = 'none';
    
    // Reseteamos los valores de los inputs a vacío
    document.getElementById('patientName').value = '';
    document.getElementById('patientAge').value = '';
    document.getElementById('modalDescription').value = '';
}

// Confirma la señal seleccionada en el modal y llama a la función para enviarla al servidor
function confirmSignal(triggerUrl, csrfToken) {
    if (selectedLevel) {
        // Llama a la función de envío asíncrono
        sendSignal(selectedLevel, triggerUrl, csrfToken);
        // Cierra la ventana emergente
        closeModal();
    }
}

// Envía los datos de la señal al servidor mediante una petición AJAX (fetch) por POST.
function sendSignal(level, triggerUrl, csrfToken) {
    // Capturamos los valores que el usuario ingresó en los inputs del modal
    const patientName = document.getElementById('patientName').value;
    const patientAge = document.getElementById('patientAge').value;
    const description = document.getElementById('modalDescription').value;

    // Creamos un objeto FormData que simula el envío de un formulario tradicional HTML
    const formData = new FormData();
    formData.append('level', level);
    formData.append('description', description);
    formData.append('patient_name', patientName);
    formData.append('patient_age', patientAge);
    // Es vital enviar el token CSRF para que Django acepte la petición POST por seguridad
    formData.append('csrfmiddlewaretoken', csrfToken);

    // Hacemos la petición HTTP asíncrona hacia la URL del backend
    fetch(triggerUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) // Convertimos la respuesta del servidor a un objeto JSON
    .then(data => {
        // Verificamos si Django nos devolvió un estado de éxito
        if (data.status === 'success') {
            // Mostramos una notificación emergente tipo "Toast"
            showToast(`Señal ${level} Desplegada`);
            
            // Añadimos el nuevo registro a la lista HTML sin tener que recargar
            addSignalToList(data);
            
            // Usamos la API de síntesis de voz para leer la alerta en voz alta
            announceSignal(level, description);
            
            // Incrementamos las estadísticas de la gráfica
            updateChart(level);
            
            // Efecto visual inmersivo: Parpadeo temporal del fondo de pantalla
            const body = document.body;
            const originalBg = body.style.backgroundColor;
            const flashColor = level === 'RED' ? '#220000' : (level === 'YELLOW' ? '#221100' : '#001100');
            body.style.backgroundColor = flashColor;
            // Después de medio segundo (500ms), volvemos al fondo original
            setTimeout(() => body.style.backgroundColor = originalBg, 500);
        }
    });
}

// Actualiza los valores de la gráfica localmente (en el cliente) cuando se dispara una nueva señal
function updateChart(level) {
    if (statsData && currentChart) {
        // Sumamos 1 al contador del nivel que se acaba de disparar
        statsData[level]++;
        
        // Asignamos el nuevo arreglo de datos a la instancia de Chart.js
        currentChart.data.datasets[0].data = [statsData.GREEN, statsData.YELLOW, statsData.RED];
        
        // Le pedimos a Chart.js que se repinte con los nuevos valores
        currentChart.update();
    }
}

// Reproduce un mensaje de voz utilizando el SpeechSynthesis API nativo del navegador
function announceSignal(level, description) {
    // Si el navegador no soporta esta tecnología, simplemente salimos de la función
    if (!('speechSynthesis' in window)) return;
    
    // Diccionario para traducir el nivel en inglés a texto audible en español
    const levelNames = {
        'GREEN': 'Código Verde, nivel bajo.',
        'YELLOW': 'Código Amarillo, nivel intermedio.',
        'RED': 'Código Rojo, nivel crítico.'
    };

    // Construimos la frase principal
    let text = `Atención. Se ha activado ${levelNames[level]}`;
    // Si hay una descripción o síntoma, lo adjuntamos al mensaje de voz
    if (description) {
        text += ` Detalles: ${description}`;
    }

    // Creamos una nueva instancia de voz con nuestro texto
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'es-ES'; // Configuramos el idioma español
    utterance.rate = 0.9;     // Velocidad ligeramente más lenta para mayor claridad
    utterance.pitch = 1;      // Tono normal
    
    // Le pedimos al navegador que empiece a hablar
    window.speechSynthesis.speak(utterance);
}

// Muestra una notificación breve (Toast) en pantalla de manera no intrusiva
function showToast(message) {
    const toast = document.getElementById('toast');
    toast.innerText = message; // Cambiamos el texto
    toast.style.display = 'block'; // Lo hacemos visible
    
    // Configuramos un temporizador para ocultarlo después de 3 segundos (3000ms)
    setTimeout(() => toast.style.display = 'none', 3000);
}

// Crea y añade un nuevo elemento HTML a la lista de actividad reciente (el historial del dashboard)
function addSignalToList(data) {
    const list = document.getElementById('signalList'); // Seleccionamos la lista (<ul>)
    const item = document.createElement('li'); // Creamos un nuevo elemento de lista (<li>)
    item.className = 'signal-item';
    
    // Definimos la etiqueta legible en función del nivel
    let label = data.level === 'GREEN' ? 'Código Verde - Bajo' : 
                (data.level === 'YELLOW' ? 'Código Amarillo - Intermedio' : 'Código Rojo - Alto');
    
    // Construimos pedazos de HTML solo si existen datos para ellos (evitar "undefined")
    let patientHtml = data.patient_name ? `<span class="patient-info-tag">Paciente: ${data.patient_name}</span>` : '';
    let descriptionHtml = data.description ? `<span class="signal-description">${data.description}</span>` : '';

    // Rellenamos el nuevo <li> con todo el marcado HTML inyectando los datos devueltos por el servidor
    item.innerHTML = `
        <div>
            <span class="level-tag tag-${data.level.toLowerCase()}">${label}</span>
            <span class="user-tag">por ${data.user}</span>
            ${patientHtml}
            ${descriptionHtml}
        </div>
        <span class="timestamp">${data.timestamp}</span>
    `;
    
    // Insertamos el nuevo registro al principio de la lista (arriba de todos los demás)
    list.insertBefore(item, list.firstChild);
    
    // Para no saturar el historial visualmente, si pasamos de 10 elementos, eliminamos el último (el más viejo)
    if (list.children.length > 10) {
        list.removeChild(list.lastChild);
    }
}
