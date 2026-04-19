/* ═══════════════════════════════════════════════════════════
   POS - Lógica del Punto de Venta | Sistema SIC
   ═══════════════════════════════════════════════════════════ */

let cart = [];
let selectedCartItemIndex = -1; // Para el teclado del sidebar

// Variables del Modal
let modalPaidValue = "";
let modalSelectedMethod = "Bolivares";
let modalPayments = []; // Para pagos mixtos

// --- EFECTOS DE SONIDO (Sintetizados) ---
function playSuccessSound() {
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(440, audioCtx.currentTime + 0.2);
        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.3);
    } catch(e) { console.log("Audio no soportado"); }
}

// Tasa BCV (Obtenida del DOM)
function getTasaBcv() {
    const el = document.getElementById('tasaBcvGlobal');
    return el ? parseFloat(el.value) || 1.0 : 1.0;
}

// 1. Añadir al Carrito
function addToCart(id, nombre, precio) {
    cart.push({
        id,
        nombre,
        precio: parseFloat(precio),
        cantidad: 1
    });
    selectedCartItemIndex = cart.length - 1;
    renderCart();
}

// 2. Renderizar Carrito
function renderCart() {
    const container = document.getElementById('cartItems');
    const tasa = getTasaBcv();

    if (cart.length === 0) {
        container.innerHTML = `
            <div class="ticket-empty">
                <i class='bx bx-shopping-bag'></i>
                <p>Esperando items...</p>
                <span class="empty-hint">Seleccione un examen del catalogo</span>
            </div>`;
        updateTotals(0);
        selectedCartItemIndex = -1;
        return;
    }

    container.innerHTML = cart.map((item, index) => {
        const itemTotalBs = item.precio * item.cantidad;
        const itemTotalUsd = itemTotalBs / tasa;
        const isSelected = index === selectedCartItemIndex ? 'selected' : '';
        
        return `
        <div class="cart-item ${isSelected}" onclick="selectCartItem(${index})">
            <div class="cart-item-info">
                <h4>${item.nombre}</h4>
                <div class="cart-item-details">
                    <span class="qty-badge">${item.cantidad}x</span>
                    <span class="unit-price">Bs. ${item.precio.toFixed(2)}</span>
                    <span class="item-total-line">Bs. ${itemTotalBs.toFixed(2)}</span>
                </div>
                <div class="item-reference-usd">Ref: $${itemTotalUsd.toFixed(2)}</div>
            </div>
            <button class="btn-remove" onclick="event.stopPropagation(); removeFromCart(${index})">
                <i class='bx bx-x-circle'></i>
            </button>
        </div>
    `}).join('');

    const total = cart.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    updateTotals(total);
}

function selectCartItem(index) {
    selectedCartItemIndex = index;
    renderCart();
}

// Teclado del Sidebar (Cantidades)
function pressSideNumpad(val) {
    if (selectedCartItemIndex === -1 && cart.length > 0) {
        selectedCartItemIndex = cart.length - 1;
    }
    
    if (selectedCartItemIndex === -1) return;

    let item = cart[selectedCartItemIndex];

    if (val === 'C') {
        item.cantidad = 1;
    } else if (val === 'DEL') {
        removeFromCart(selectedCartItemIndex);
        return;
    } else {
        let currentQty = item.cantidad.toString();
        if (currentQty === "1" && val !== "0") {
            currentQty = val; 
        } else {
            currentQty += val;
        }
        
        let newQty = parseInt(currentQty);
        if (isNaN(newQty) || newQty <= 0) newQty = 1;
        if (newQty > 99) newQty = 99;
        item.cantidad = newQty;
    }
    renderCart();
}

// 3. Eliminar del Carrito
function removeFromCart(index) {
    cart.splice(index, 1);
    if (selectedCartItemIndex >= cart.length) {
        selectedCartItemIndex = cart.length - 1;
    }
    renderCart();
}

// 4. Actualizar Totales
function updateTotals(totalBs) {
    const tasa = getTasaBcv();
    const totalUsd = totalBs / tasa;
    
    document.getElementById('subtotal').innerText = `Bs. ${totalBs.toFixed(2)}`;
    document.getElementById('total').innerHTML = `
        <div class="total-main">Bs. ${totalBs.toFixed(2)}</div>
        <div class="total-sub-usd">Equivalente: $${totalUsd.toFixed(2)}</div>
    `;
}

// 5. Filtrar Exámenes por texto
function filterExams() {
    const q = document.getElementById('searchExam').value.toLowerCase();
    const tiles = document.querySelectorAll('.exam-tile');
    tiles.forEach(tile => {
        const text = tile.querySelector('.tile-name').innerText.toLowerCase();
        tile.style.display = text.includes(q) ? 'flex' : 'none';
    });
}

/* ═══════════════════════════════════════════════════════════
   LÓGICA DEL MODAL DE PAGO (PAGOS MIXTOS)
   ═══════════════════════════════════════════════════════════ */

function abrirModalPago() {
    if (cart.length === 0) {
        alert("El carrito está vacío");
        return;
    }

    const tasa = getTasaBcv();
    const totalBs = cart.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    const totalUsd = totalBs / tasa;

    document.getElementById('modalTotalToPay').innerHTML = `
        <span>Bs. ${totalBs.toFixed(2)}</span>
        <small style="display:block; font-size: 0.6em; opacity: 0.7;">($${totalUsd.toFixed(2)})</small>
    `;
    document.getElementById('modalSummaryPending').innerText = `Bs. ${totalBs.toFixed(2)}`;
    
    // Resetear variables del modal
    modalPaidValue = "";
    modalSelectedMethod = "Bolivares";
    modalPayments = [];
    document.getElementById('modalPaidAmount').innerText = "0.00";
    document.getElementById('modalSummaryRegistered').innerText = "Bs. 0.00";
    document.getElementById('modalPaymentsList').innerHTML = '<div class="empty-payments">No hay pagos agregados</div>';
    
    document.querySelectorAll('.method-card').forEach(c => {
        c.classList.toggle('active', c.getAttribute('data-method') === 'Bolivares');
    });

    document.getElementById('paymentModal').style.display = 'flex';
}

function cerrarModalPago() {
    document.getElementById('paymentModal').style.display = 'none';
}

function pressNumModal(val) {
    if (val === 'C') {
        modalPaidValue = "";
    } else if (val === '.') {
        if (!modalPaidValue.includes('.')) modalPaidValue += val;
    } else {
        const dotIndex = modalPaidValue.indexOf('.');
        if (dotIndex !== -1 && modalPaidValue.length - dotIndex > 2) return;
        modalPaidValue += val;
    }
    
    const tasa = getTasaBcv();
    const montoBs = parseFloat(modalPaidValue) || 0;
    const montoUsd = montoBs / tasa;
    
    document.getElementById('modalPaidAmount').innerHTML = `
        ${modalPaidValue || "0.00"}
        <span style="font-size: 0.4em; color: var(--pos-text-muted); display: block;">≈ $${montoUsd.toFixed(2)}</span>
    `;
}

function setMethodModal(method, element) {
    modalSelectedMethod = method;
    document.querySelectorAll('.method-card').forEach(c => c.classList.remove('active'));
    element.classList.add('active');
}

// PAGOS MIXTOS: Agregar a la lista
function agregarPagoMixto() {
    let monto = parseFloat(modalPaidValue);
    const tasa = getTasaBcv();

    if (isNaN(monto) || monto <= 0) {
        alert("Ingrese un monto válido");
        return;
    }

    if (modalSelectedMethod === "Divisa") {
        monto = Math.round((monto * tasa) * 100) / 100;
    }

    const totalVenta = cart.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    const pagadoYa = modalPayments.reduce((sum, p) => sum + p.monto, 0);
    const pendiente = totalVenta - pagadoYa;

    if (monto > (pendiente + 0.01)) {
        if (!confirm("El monto ingresado es mayor al saldo pendiente. ¿Desea agregarlo de todas formas?")) {
            return;
        }
    }

    modalPayments.push({
        metodo: modalSelectedMethod,
        monto: monto,
        montoUsd: (modalSelectedMethod === "Divisa") ? parseFloat(modalPaidValue) : null
    });

    modalPaidValue = "";
    document.getElementById('modalPaidAmount').innerText = "0.00";
    
    window.isNewPayment = true; 
    renderModalPayments();
    setTimeout(() => { window.isNewPayment = false; }, 100);
}

function quitarPagoMixto(index) {
    modalPayments.splice(index, 1);
    renderModalPayments();
}

function renderModalPayments() {
    const container = document.getElementById('modalPaymentsList');
    
    const totalVenta = cart.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    const pagadoYa = modalPayments.reduce((sum, p) => sum + p.monto, 0);
    const diferencia = pagadoYa - totalVenta;

    if (modalPayments.length === 0) {
        container.innerHTML = '<div class="empty-payments">No hay pagos agregados</div>';
    } else {
        container.innerHTML = modalPayments.map((p, i) => {
            const isVuelto = p.monto < 0;
            return `
                <div class="payment-item ${isVuelto ? 'item-negativo-lista' : ''}">
                    <div class="method-info">
                        <i class='bx ${getIconForMethod(p.metodo)}'></i>
                        <span>${p.metodo} ${p.montoUsd ? `($${p.montoUsd.toFixed(2)})` : ''}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span class="amount-info">Bs. ${p.monto.toFixed(2)}</span>
                        <i class='bx bx-trash btn-remove-pago' onclick="quitarPagoMixto(${i})"></i>
                    </div>
                </div>
            `}).join('');
        
        if (diferencia > 0.005) {
            container.innerHTML += `
                <div class="payment-item item-cambio-lista">
                    <div class="method-info">
                        <span><b>CAMBIO</b></span>
                    </div>
                    <div class="change-detail-list">
                        <span style="font-size: 1.1em;"><b>${diferencia.toFixed(2)}bs</b></span>
                    </div>
                </div>
            `;
        }
    }

    document.getElementById('modalSummaryRegistered').innerText = `Bs. ${pagadoYa.toFixed(2)}`;
    
    const labelPending = document.getElementById('labelPending');
    const displayPending = document.getElementById('modalSummaryPending');
    const boxPending = document.getElementById('boxPending');

    if (diferencia > 0.005) {
        labelPending.innerText = "Vuelto Pendiente:";
        displayPending.innerText = `Bs. ${diferencia.toFixed(2)}`;
        displayPending.style.color = "#10b981"; 
        boxPending.classList.add('pulse-success');
        if (typeof isNewPayment !== 'undefined' && isNewPayment) playSuccessSound();
    } else if (Math.abs(diferencia) <= 0.005) {
        labelPending.innerText = "Estado:";
        displayPending.innerText = "¡LISTO PARA FINALIZAR!";
        displayPending.style.color = "#10b981";
        boxPending.classList.remove('pulse-success');
        if (typeof isNewPayment !== 'undefined' && isNewPayment) playSuccessSound();
    } else {
        labelPending.innerText = "Pendiente:";
        displayPending.innerText = `Bs. ${Math.abs(diferencia).toFixed(2)}`;
        displayPending.style.color = "#dc2626"; 
        boxPending.classList.remove('pulse-success');
    }

    const btnAction = document.getElementById('btnMainAction');
    if (diferencia > 0.005) {
        // Estado: Hay vuelto por entregar
        btnAction.innerHTML = "<i class='bx bx-money-withdraw'></i> REGISTRAR VUELTO";
        btnAction.onclick = agregarVueltoManual;
        btnAction.classList.add('ready-to-finish');
    } else if (Math.abs(diferencia) <= 0.005 && modalPayments.length > 0) {
        // Estado: Balance en cero, listo para confirmar
        btnAction.innerHTML = "<i class='bx bx-check-double'></i> FINALIZAR VENTA";
        btnAction.onclick = finalizarVenta;
        btnAction.classList.add('ready-to-finish');
    } else {
        // Estado: Falta dinero
        btnAction.innerHTML = "<i class='bx bx-plus'></i> AÑADIR PAGO";
        btnAction.onclick = agregarPagoMixto;
        btnAction.classList.remove('ready-to-finish');
    }
}

function agregarVueltoManual() {
    const totalVenta = cart.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    const pagadoYa = modalPayments.reduce((sum, p) => sum + p.monto, 0);
    const diferencia = pagadoYa - totalVenta;

    if (diferencia <= 0.005) return;

    const montoManual = parseFloat(modalPaidValue) || 0;

    // Validación obligatoria
    if (Math.abs(montoManual - diferencia) > 0.01) {
        alert(`⚠️ Verificación de Vuelto:\nEl monto escrito (${montoManual.toFixed(2)}) no coincide con el vuelto calculado (${diferencia.toFixed(2)}).\nEscriba el monto exacto para continuar.`);
        return;
    }

    // Agregar el pago NEGATIVO (Vuelto entregado)
    modalPayments.push({
        metodo: modalSelectedMethod + " (Vuelto)",
        monto: -montoManual,
        montoUsd: null
    });

    modalPaidValue = "";
    document.getElementById('modalPaidAmount').innerText = "0.00";
    renderModalPayments();
}

function getIconForMethod(method) {
    if (method && method.includes("Vuelto")) return 'bx-undo';
    const icons = {
        'Bolivares': 'bx-money',
        'Divisa': 'bx-dollar-circle',
        'Debito': 'bx-credit-card',
        'Credito': 'bx-credit-card-alt',
        'Pago Movil': 'bx-mobile-vibration'
    };
    return icons[method] || 'bx-wallet';
}

function pagoExacto() {
    const totalVenta = cart.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    const pagadoYa = modalPayments.reduce((sum, p) => sum + p.monto, 0);
    const pendiente = totalVenta - pagadoYa;

    if (pendiente <= 0) return;

    modalPaidValue = pendiente.toFixed(2);
    const tasa = getTasaBcv();
    const montoUsd = pendiente / tasa;
    
    document.getElementById('modalPaidAmount').innerHTML = `
        ${modalPaidValue}
        <span style="font-size: 0.4em; color: var(--pos-text-muted); display: block;">≈ $${montoUsd.toFixed(2)}</span>
    `;
}

async function finalizarVenta() {
    const paciente = document.getElementById('pacienteNombre').value;
    if (!paciente) {
        alert("Seleccione un paciente.");
        return;
    }

    const data = {
        paciente: paciente,
        items: cart.map(i => ({ id: i.id, nombre: i.nombre, precio: i.precio, cantidad: i.cantidad })),
        total: cart.reduce((sum, item) => sum + (item.precio * item.cantidad), 0),
        pagos: modalPayments
    };

    try {
        const response = await fetch('/pos/validar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        if (result.status === 'success') {
            cerrarModalPago();
            mostrarModalExito(0); // El cambio ya se registró como pago negativo
        } else {
            alert("Error: " + result.message);
        }
    } catch (e) {
        alert("Error de conexión");
    }
}

function mostrarModalExito(cambio) {
    const modal = document.getElementById('modalSuccess');
    const timerText = document.getElementById('successTimer');
    const progressBar = document.getElementById('successProgressBar');

    modal.style.display = 'flex';
    progressBar.classList.add('animate-timer');

    let seconds = 3;
    timerText.innerText = seconds;
    const interval = setInterval(() => {
        seconds--;
        timerText.innerText = seconds;
        if (seconds <= 0) {
            clearInterval(interval);
            resetearPOS();
        }
    }, 1000);
}

function resetearPOS() {
    document.getElementById('modalSuccess').style.display = 'none';
    cart = [];
    selectedCartItemIndex = -1;
    modalPayments = [];
    document.getElementById('pacienteNombre').value = "";
    document.getElementById('successProgressBar').classList.remove('animate-timer');
    renderCart();
}
