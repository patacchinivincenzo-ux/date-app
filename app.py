import os
from flask import Flask

# Forziamo Flask a capire che la cartella 'static' è esattamente nella stessa cartella del codice
app = Flask(__name__, static_folder='static', static_url_path='/static')

HTML = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Date Game</title>

    <style>
    body {
        margin: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        background: linear-gradient(135deg, #ffdde1, #ee9ca7);
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        text-align: center;
    }

    .card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 25px;
        border-radius: 25px;
        width: 85%;
        max-width: 350px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    .profile-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        margin: 0 auto 15px auto;
        border: 3px solid white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        display: block;
    }

    /* FIX iOS & STILE CALENDARIO */
    input[type="date"] {
        background-color: white !important;
        color: #ff4d6d !important;
        border: none;
        padding: 12px;
        border-radius: 12px;
        font-weight: 600;
        font-family: inherit;
        font-size: 1rem;
        outline: none;
        margin: 15px 0;
        width: 80%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        -webkit-appearance: none; /* Forza lo stile su iOS */
        min-height: 20px;
    }

    button {
        margin: 10px;
        padding: 12px 24px;
        border: none;
        border-radius: 15px;
        background: white;
        color: #ff4d6d;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    button:hover {
        transform: scale(1.05);
        background: #fff0f2;
    }

    /* FEEDBACK VISIVO PER BOTTONE DISABILITATO */
    button:disabled {
        background: rgba(255, 255, 255, 0.3) !important;
        color: rgba(255, 255, 255, 0.6) !important;
        cursor: not-allowed;
        transform: none;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .resoconto-box {
        background: rgba(255, 255, 255, 0.2);
        padding: 15px;
        border-radius: 15px;
        margin-top: 15px;
        border: 1px dashed rgba(255, 255, 255, 0.4);
        text-align: left;
    }

    .lettera-amore {
        font-size: 1rem;
        line-height: 1.5;
        margin: 15px 0;
        text-align: center;
        font-weight: 500;
    }

    .screen { display: none; }
    .active { display: block; }
    </style>
</head>

<body>

<div class="card">
    <img src="/static/noi.jpg" alt="Noi" class="profile-img">

    <div id="s1" class="screen active">
        <h2>Quando usciamo? ❤️</h2>
        <input type="date" id="date-picker" onchange="checkDate()">
        <br>
        <button id="next-btn" onclick="go(2)" disabled>Continua</button>
    </div>

    <div id="s2" class="screen">
        <h3>Cosa ti va di fare?</h3>
        <button onclick="go(3,'🍝 Mangiare')">🍝 Mangiare</button>
        <button onclick="go(3,'🎬 Cinema')">🎬 Cinema</button>
        <button onclick="go(3,'🚶 Passeggiata')">🚶 Passeggiata</button>
    </div>

    <div id="s3" class="screen">
        <h3>Ti piace come programma?</h3>
        <p id="text" style="font-weight: bold; font-size: 1.1em; line-height: 1.5;"></p>
        <button onclick="final()">Conferma data ❤️</button>
    </div>

    <div id="s4" class="screen">
        <h2>Perfetto ❤️</h2>
        
        <div class="lettera-amore">
            Scusami se a volte ho sbagliato atteggiamento o sono stato difficile.<br><br>
            Non cambia quello che provo per te.<br><br>
            Tu sei una persona davvero importante e speciale per me.<br><br>
            Io ti amo, e voglio davvero stare con te.<br><br>
            Sei una parte della mia vita che non voglio perdere.<br><br>
            <strong>Ti amo ❤️</strong><br>
            <em>Baka.</em>
        </div>
        
        <div class="resoconto-box">
            <p style="margin: 5px 0; font-weight: bold; text-align:center;">📋 IL NOSTRO APPUNTAMENTO:</p>
            <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.3); margin: 10px 0;">
            <p><strong>📅 Data:</strong> <span id="summary-date"></span></p>
            <p><strong>✨ Attività:</strong> <span id="summary-choice"></span></p>
        </div>
    </div>

</div>

<script>
let dataSelezionata = "";
let sceltaSelezionata = "";

const oggi = new Date().toISOString().split('T')[0];
document.getElementById('date-picker').min = oggi;

function checkDate() {
    const dateInput = document.getElementById('date-picker').value;
    const nextBtn = document.getElementById('next-btn');
    if (dateInput) {
        dataSelezionata = formatDate(dateInput);
        nextBtn.disabled = false;
    } else {
        nextBtn.disabled = true;
    }
}

function formatDate(dateString) {
    const parti = dateString.split('-');
    return parti[2] + '/' + parti[1] + '/' + parti[0];
}

function go(screen, choice) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById('s' + screen).classList.add('active');

    if (choice) {
        sceltaSelezionata = choice;
    }

    if (screen === 3) {
        document.getElementById('text').innerHTML = "Il <span style='color:#ff4d6d; background:white; padding:2px 8px; border-radius:5px;'>" + dataSelezionata + "</span><br>per fare: <span style='color:#ff4d6d; background:white; padding:2px 8px; border-radius:5px;'> " + sceltaSelezionata + "</span>";
    }
}

function final() {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById('s4').classList.add('active');
    
    document.getElementById('summary-date').innerText = dataSelezionata;
    document.getElementById('summary-choice').innerText = sceltaSelezionata;
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return HTML

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)