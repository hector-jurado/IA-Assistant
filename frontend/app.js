const API_URL = "http://127.0.0.1:8000/api/chat"
const SESSION_ID =localStorage.getItem("jarvis_session_id") || "user_" + Math.random().toString(36).substr(2,9);
localStorage.setItem("jarvis_session_id", SESSION_ID)
const messagesDiv = document.getElementById("messages");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send-btn");
const statusText = document.getElementById("status-text");
const statusDot = document.querySelector(".status-dot");
const waveform = document.getElementById("waveform");
const waveCanvas = document.getElementById("wave-canvas");
const waveCtx = waveCanvas.getContext("2d");
const cpuVal = document.getElementById("cpu-val")
const cpuBar= document.getElementById("cpu-bar")
const ramVal = document.getElementById("ram-val")
const ramBar = document.getElementById("ram-bar")

// ── Anillos animados ─────────────────────────────────────────────────────────
const ringsCanvas = document.getElementById("rings");
const rCtx = ringsCanvas.getContext("2d");
let ringsAngle = 0;

function resizeRings(){
    ringsCanvas.width = window.innerWidth;
    ringsCanvas.height = window.innerHeight;
}
resizeRings();
window.addEventListener("resize", resizeRings);

function drawRings() {
    const w = ringsCanvas.width;
    const h = ringsCanvas.height;
    const cx = w * 0.78;
    const cy = h * 0.5;

    rCtx.clearRect(0, 0, w, h);
    ringsAngle += 0.003;

    const rings = [
        {r: 180, speed: 1, dash: [60, 20]},
        {r: 240, speed: -0.7, dash: [40, 30]},
        {r: 300, speed: 0.5, dash: [80, 15]},
        {r: 360, speed: -0.3, dash: [20, 40]},
    ];

    rings.forEach(rings => {
        rCtx.save();
        rCtx.translate(cx, cy);
        rCtx.rotate(ringsAngle * rings.speed);
        rCtx.beginPath();
        rCtx.arc(0, 0, rings.r, 0, Math.PI * 2);
        rCtx.setLineDash(rings.dash);
        rCtx.strokeStyle = "#00c8ff";
        rCtx.lineWidth = 1;
        rCtx.stroke();
        rCtx.restore();

    });
    requestAnimationFrame(drawRings);
}
drawRings();
// ── Stats en tiempo real (simulado) ─────────────────────────────────────────
function updateStats(){
// Simulamos valores oscilantes — en producción llamarías a un endpoint
const cpu = Math.floor(15 + Math.random() * 30)
const ram = Math.floor(40 + Math.random() * 25)

cpuVal.textContent = cpu + "%";
cpuBar.style.width = cpu + "%";
ramVal.textContent = ram + "%";
ramBar.style.width = ram + "%"
}
updateStats();
setInterval(updateStats,3000);

// ── Ondas de audio ───────────────────────────────────────────────────────────
let waveActive = false;
let waveAnimd = null;
const waveBars = 48;

function drawWave() {
    const w = waveCanvas.offsetWidth;
    const h = waveCanvas.offsetHeight;
    waveCanvas.width = w;
    waveCanvas.height = h;
    waveCtx.clearRect(0,0,w,h);

    const barW = w/waveBars;
    const t = Date.now() / 200;

    for (let i = 0; i < waveBars; i++) {
        const amp = waveActive
            ? (Math.sin(t + i * 0.4) * 0.5 + 0.5) * (h * 0.8)
            : (Math.sin(t + 0.3 + i * 0.3) * 0.5 + 0.5) * (h * 0.15)
        const x = i * barW + barW * 0.2;
        const barH = Math.max(2, amp);
        const y = (h - barH) / 2;

        waveCtx.fillStyle = "#00c8ff";
        waveCtx.globalAlpha = 0.6 + (amp / h ) * 0.4;
        waveCtx.fillRect(x, y, barW * 0.6, barH);
    }
    waveAnimd = requestAnimationFrame(drawWave);
}
drawWave()

function setWaveActive(active){
    waveActive = active;
    waveform.classList.toggle("active", active);
}

// ── Typewriter ───────────────────────────────────────────────────────────────

function typewriter(element, text, speed = 18){
    return new Promise(resolve => {
        let i = 0;
        element.textContent = "";
        const interval = setInterval(() =>{
            element.textContent += text[i];
            i++;
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
              if (i >= text.length) {
                clearInterval(interval);
                resolve();
              }
        }, speed);
    });
}

//añade un mensaje al chhat
function addMessage(role, content, animate = false) {
    const div = document.createElement("div");
    div.className  =`message message--${role}`;
    const bubble = document.createElement("div");
    bubble.className = "message__bubble";
    div.appendChild(bubble)
    messagesDiv.appendChild(div);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    if (animate && role === "assistant"){
        div.classList.add("typing");
        return {div, bubble}
    }
    bubble.textContent = content;
    return {div, bubble};
}

//Cambia el estado del header
function setStatus(thinking){
    if(thinking) {
        statusDot.classList.add("thinking");
        statusText.textContent= "PROCESANDO";
        setWaveActive(true)
    } else{
        statusDot.classList.remove("thinking")
        statusText.textContent="ONLINE";
        setWaveActive(false)
    }
}

//Envia el mensaje al backend

async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    input.value  ="";
    sendBtn.disabled = true;
    setStatus(true);

//Mostrar mensaje del usuario
addMessage("user",text);

//Mostrar indicador de escritura
const {div, bubble} = addMessage("assistant", "", true);

try {
    const res = await fetch(API_URL, {
        method: "POST",
        headers :{"Content-Type": "application/json"},
        body: JSON.stringify({message: text, session_id:SESSION_ID})
    });
    const data = await res.json();

    //Reemplazar indicador por respuesta real

     div.classList.remove("typing");
     await typewriter(bubble, data.response, 16);

  } catch (err) {
    div.classList.remove("typing");
    bubble.textContent = "ERROR: Conexión con JARVIS perdida.";
  } finally {
    setStatus(false);
    sendBtn.disabled = false;
    input.focus();
  }
}

//Eventos
sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", e => {
    if (e.key === "Enter") sendMessage();
});

// ── Micrófono ────────────────────────────────────────────────────────────────
const micBTN = document.getElementById("mic-btn");

micBTN.addEventListener("click", async()=> {
    micBTN.classList.add("recording");
    micBTN.textContent= "⏹";
    setStatus(true);

    try {
        const res = await fetch("http://127.0.0.1:8000/api/escuchar",  {
            method: "POST"
        });
        const data = await res.json();
        if (data.texto && data.texto.trim() !== ""){
            //pone el texto escuchando en el input y envia
            input.value = data.texto;
            sendMessage();
        } else {
            addMessage("assistant", "No he podido escucharte, señor. Intentelo de nuevo")
        }
    } catch (err){
        addMessage("assistant", "Error de conexión con el micrófono");
    } finally {
        micBTN.classList.remove("recording");
        micBTN.textContent = "🎤"
        setStatus(false)
    }
});

//Foco automatico al cargar
input.focus();