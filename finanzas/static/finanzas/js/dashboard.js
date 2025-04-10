document.addEventListener('DOMContentLoaded', function() {
    const tipoTransaccionSelect = document.getElementById('tipo_transaccion');
    const ingresoFields = document.getElementById('ingresoFields');
    const gastoFields = document.getElementById('gastoFields');
    const activoFields = document.getElementById('activoFields');
    const deudaFields = document.getElementById('deudaFields');
    const combinedForm = document.getElementById('combinedForm');
    const mensajeDiv = document.getElementById('mensaje');
    const financialChartCanvas = document.getElementById('financialChart').getContext('2d');
    let financialChart; // Variable para la instancia del gráfico

    function mostrarCampos(tipo) {
        ingresoFields.style.display = (tipo === 'ingreso') ? 'block' : 'none';
        gastoFields.style.display = (tipo === 'gasto') ? 'block' : 'none';
        activoFields.style.display = (tipo === 'activo') ? 'block' : 'none';
        deudaFields.style.display = (tipo === 'deuda') ? 'block' : 'none';
    }

    mostrarCampos('');

    tipoTransaccionSelect.addEventListener('change', function() {
        mostrarCampos(this.value);
    });

    combinedForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const tipoTransaccion = tipoTransaccionSelect.value;
        let data = {};

        if (tipoTransaccion === 'ingreso') {
            data = {
                tipo_transaccion: tipoTransaccion,
                montoMensual: document.getElementById('montoMensual').value,
                esVariable: document.getElementById('esVariable').checked
            };
        } else if (tipoTransaccion === 'gasto') {
            data = {
                tipo_transaccion: tipoTransaccion,
                monto: document.getElementById('gasto_monto').value
            };
        } else if (tipoTransaccion === 'activo') {
            data = {
                tipo_transaccion: tipoTransaccion,
                valorActivo: document.getElementById('valorActivo').value,
                generaIngresosPasivos: document.getElementById('generaIngresosPasivos').checked
            };
        } else if (tipoTransaccion === 'deuda') {
            data = {
                tipo_transaccion: tipoTransaccion,
                tipo_cuota: document.getElementById('tipo_cuota').checked,
                numero_total_cuotas: document.getElementById('numero_total_cuotas').value,
                cuotas_restantes: document.getElementById('cuotas_restantes').value,
                pago_mensual: document.getElementById('pago_mensual').value,
                saldo_pendiente: document.getElementById('saldo_pendiente').value
            };
        }

        const url = this.dataset.url;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            mensajeDiv.textContent = result.message;
            if (result.success) {
                combinedForm.reset();
                mostrarCampos('');
                actualizarGrafica(result.dashboard_data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            mensajeDiv.textContent = 'Error al agregar la transacción.';
        });
    });

    function actualizarGrafica(data) {
        const labels = ['Ingresos', 'Gastos', 'Activos', 'Deudas'];
        const ingresos = data ? data.ingresos_total : 0;
        const gastos = data ? data.gastos_total : 0;
        const activos = data ? data.activos_total : 0;
        const deudas = data ? data.deudas_total : 0;

        const dataGrafica = {
            labels: labels,
            datasets: [{
                label: 'Resumen Financiero',
                data: [ingresos, -gastos, activos, -deudas], // Gastos y deudas como valores negativos para visualización
                backgroundColor: [
                    'rgba(75, 192, 192, 0.5)', // Ingresos (Verde)
                    'rgba(255, 99, 132, 0.5)',  // Gastos (Rojo)
                    'rgba(255, 206, 86, 0.5)', // Activos (Amarillo)
                    'rgba(54, 162, 235, 0.5)'  // Deudas (Azul)
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 1
            }]
        };

        const config = {
            type: 'bar',
            data: dataGrafica,
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        };

        if (financialChart) {
            financialChart.destroy();
        }
        financialChart = new Chart(financialChartCanvas, config);
    }

    // Simulación de datos iniciales
    actualizarGrafica({ ingresos_total: 0, gastos_total: 0, activos_total: 0, deudas_total: 0 });
});