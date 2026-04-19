// VISOR BIOMÉTRICO 3D - VERSIÓN ESTABLE Y ROBUSTA
// Carga global (no módulos) para máxima compatibilidad

let scene, camera, renderer, body, controls, baseMeshes = [];
let rotateModel = true;
let isFemenino = false;
let skeleton, organs;
let skeletonActive = false;
let organsActive = false;
let skeletonLoading = false;
let organsLoading = false;

function init() {
    console.log("Iniciando Visor Biométrico...");
    const container = document.getElementById('three-container');
    const loaderElement = document.getElementById('loader');

    if (!container) return;

    if (typeof THREE === 'undefined') {
        console.error("THREE no definido");
        if (loaderElement) loaderElement.innerHTML = "<p style='color:red'>❌ Error de conexión: No se pudo cargar Three.js</p>";
        return;
    }

    try {
        const sexAttr = container.getAttribute('data-sex') || 'masculino';
        const sex = sexAttr.trim().toLowerCase();
        isFemenino = (sex.includes('fem') || sex.includes('muj'));

        scene = new THREE.Scene();
        scene.background = new THREE.Color(0xdbeafe);

        camera = new THREE.PerspectiveCamera(40, container.clientWidth / container.clientHeight, 0.1, 1000);

        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.outputEncoding = THREE.sRGBEncoding;
        container.appendChild(renderer.domElement);

        // Los controles y cargadores en modo global suelen colgar de THREE.*
        const OrbitCtrl = THREE.OrbitControls || OrbitControls;
        controls = new OrbitCtrl(camera, renderer.domElement);
        controls.enableDamping = true;

        setupLights();
        loadMainModel(sex);
        animate();
        
        console.log("Visor inicializado correctamente.");
    } catch (e) {
        console.error("Error init:", e);
        if (loaderElement) loaderElement.innerHTML = `<p style='color:red'>❌ Error:<br>${e.message}</p>`;
    }
}

function setupLights() {
    scene.add(new THREE.AmbientLight(0xffffff, 0.4));
    const keyLight = new THREE.DirectionalLight(0xffffff, 2.2);
    keyLight.position.set(1, 6, 4);
    scene.add(keyLight);
    const fillLight = new THREE.DirectionalLight(0x8899cc, 0.6);
    fillLight.position.set(-4, 2, -2);
    scene.add(fillLight);
}

function loadMainModel(sex) {
    const loaderElement = document.getElementById('loader');
    const LoaderClass = THREE.GLTFLoader || GLTFLoader;
    const loader = new LoaderClass();

    let path = '/static/models/cuerpo_masculino.glb';
    if (sex.includes('fem') || sex.includes('muj') || sex.includes('girl')) {
        path = '/static/models/cuerpo_femenino.glb';
    }

    const loadWithFallback = (targetPath, isRetry = false) => {
        loader.load(targetPath, (gltf) => {
            body = gltf.scene;
            scene.add(body);
            
            body.traverse((child) => {
                if (child.isMesh) {
                    child.material = new THREE.MeshStandardMaterial({
                        color: 0x718096,
                        roughness: 0.7
                    });
                    baseMeshes.push(child);
                }
            });

            // Centrado físico
            body.updateMatrixWorld(true);
            const box = new THREE.Box3().setFromObject(body);
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());
            body.position.sub(center);

            // Posicionar cámara
            const maxDim = Math.max(size.x, size.y, size.z);
            const fov = camera.fov * (Math.PI / 180);
            let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2)) * 1.5;
            camera.position.set(0, 0, cameraZ);
            controls.target.set(0, 0, 0);

            if (loaderElement) loaderElement.style.display = 'none';
        }, undefined, (err) => {
            console.error("Error carga:", targetPath, err);
            if (!isRetry && targetPath.includes('femenino')) {
                loadWithFallback('/static/models/cuerpo_masculino.glb', true);
            } else {
                if (loaderElement) loaderElement.innerHTML = `<p style='color:red'>❌ Error al cargar modelo principal</p>`;
            }
        });
    };

    loadWithFallback(path);
}

function fitLayerToBody(layer) {
    if (!layer || !body) return;
    
    // Asegurar que el cuerpo tenga sus transformaciones al día
    body.updateMatrixWorld(true);
    layer.updateMatrixWorld(true);

    // Calcular cajas basadas solo en mallas para evitar errores de contenedores vacíos
    const bodyBox = new THREE.Box3().setFromObject(body);
    const layerBox = new THREE.Box3().setFromObject(layer);

    const bodySize = bodyBox.getSize(new THREE.Vector3());
    const layerSize = layerBox.getSize(new THREE.Vector3());

    if (layerSize.y === 0) return;

    // Calcular ratio de escala (96% para un ajuste interno cómodo)
    const ratio = bodySize.y / layerSize.y;
    const finalScale = ratio * 0.96;
    layer.scale.set(finalScale, finalScale, finalScale);

    // Re-calcular caja después de escalar
    layer.updateMatrixWorld(true);
    const updatedLayerBox = new THREE.Box3().setFromObject(layer);
    
    // Alineación central total
    const bodyCenter = bodyBox.getCenter(new THREE.Vector3());
    const layerCenter = updatedLayerBox.getCenter(new THREE.Vector3());

    // El offset necesario para que el centro de la capa coincida con el centro del cuerpo
    const offset = new THREE.Vector3().subVectors(bodyCenter, layerCenter);
    layer.position.add(offset);
}

function animate() {
    requestAnimationFrame(animate);
    const speed = 0.004;
    if (body && rotateModel) body.rotation.y += speed;
    if (skeleton && rotateModel) skeleton.rotation.y += speed;
    if (organs && rotateModel) organs.rotation.y += speed;
    if (controls) controls.update();
    if (renderer && scene && camera) renderer.render(scene, camera);
}

// Botones y Sliders
document.getElementById('btn-skeleton').onclick = function() {
    if (skeletonLoading) return;
    if (!skeleton) {
        skeletonLoading = true;
        this.innerHTML = "<i class='bx bx-loader-alt bx-spin'></i>";
        const LoaderClass = THREE.GLTFLoader || GLTFLoader;
        new LoaderClass().load('/static/models/esqueleto.glb', (gltf) => {
            skeleton = gltf.scene;
            scene.add(skeleton);
            skeleton.traverse(c => { if(c.isMesh) c.material.color.set(0xffffff); });
            fitLayerToBody(skeleton);
            skeletonLoading = false;
            skeletonActive = true;
            this.innerHTML = "<i class='bx bx-bone'></i>";
            updateView();
        });
    } else {
        skeletonActive = !skeletonActive;
        updateView();
    }
};

document.getElementById('btn-organs').onclick = function() {
    if (organsLoading) return;
    if (!organs) {
        organsLoading = true;
        this.innerHTML = "<i class='bx bx-loader-alt bx-spin'></i>";
        const LoaderClass = THREE.GLTFLoader || GLTFLoader;
        new LoaderClass().load('/static/models/organos.glb', (gltf) => {
            organs = gltf.scene;
            scene.add(organs);
            fitLayerToBody(organs);
            organsLoading = false;
            organsActive = true;
            this.innerHTML = "<i class='bx bx-circle'></i>";
            updateView();
        });
    } else {
        organsActive = !organsActive;
        updateView();
    }
};

function updateView() {
    const isAny = skeletonActive || organsActive;
    if (body) {
        // En lugar de transparencia, ocultamos el cuerpo totalmente para mayor claridad
        body.visible = !isAny;
    }
    if (skeleton) skeleton.visible = skeletonActive;
    if (organs) organs.visible = organsActive;

    document.getElementById('btn-skeleton').style.background = skeletonActive ? '#2dd4bf' : 'rgba(45, 212, 191, 0.2)';
    document.getElementById('btn-skeleton').style.color = skeletonActive ? '#ffffff' : '#2dd4bf';
    document.getElementById('btn-organs').style.background = organsActive ? '#a78bfa' : 'rgba(167, 139, 250, 0.2)';
    document.getElementById('btn-organs').style.color = organsActive ? '#ffffff' : '#a78bfa';
}

window.resetCamera = () => {
    if (!body) return;
    body.rotation.y = 0;
    if (skeleton) skeleton.rotation.y = 0;
    if (organs) organs.rotation.y = 0;
    init(); // Reinicio rápido de cámara
};

document.getElementById('toggle-rotation').onclick = () => rotateModel = !rotateModel;

document.getElementById('weight-slider').oninput = (e) => {
    const v = parseInt(e.target.value);
    document.getElementById('weight-val').innerText = v;
    const s = 1 + (v - 70) / 160;
    if (body) body.scale.set(s, 1, s);
    if (skeleton) {
        fitLayerToBody(skeleton); // Re-ajustar tras cambio de escala
        skeleton.scale.set(skeleton.scale.x * s, skeleton.scale.y, skeleton.scale.z * s);
    }
};

document.getElementById('temp-slider').oninput = (e) => {
    const v = parseFloat(e.target.value);
    document.getElementById('temp-val').innerText = v;
    baseMeshes.forEach(m => {
        if (v > 37.5) {
            m.material.emissive = new THREE.Color(0xff2200);
            m.material.emissiveIntensity = ((v - 37.5) / 4) * 0.6;
        } else {
            m.material.emissive = new THREE.Color(0,0,0);
            m.material.emissiveIntensity = 0;
        }
    });
};

window.addEventListener('load', init);
window.addEventListener('resize', () => {
    const container = document.getElementById('three-container');
    if (camera && renderer && container) {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    }
});
