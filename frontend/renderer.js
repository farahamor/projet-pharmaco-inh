const btnCalculer = document.getElementById("btnCalculer");
const btnRecommandation = document.getElementById("btnRecommandation");

let patientData = {};
let dp = null;

btnCalculer.addEventListener("click", () => {

    const poids = parseFloat(document.getElementById("poids").value);
    const dose = parseFloat(document.getElementById("dose").value);
    const c3 = parseFloat(document.getElementById("c3").value);

    if (!poids || poids <= 0) {
        alert("Veuillez saisir un poids valide.");
        return;
    }

    if (!dose || dose <= 0) {
        alert("Veuillez saisir une dose valide.");
        return;
    }

    if (!c3 || c3 <= 0) {
        alert("Veuillez saisir une concentration C3 valide.");
        return;
    }

    dp = dose / poids;

    document.getElementById("dpValue").textContent =
        dp.toFixed(4);

    document.getElementById("resultatDP")
        .classList.remove("hidden");

    patientData = {
        nom: document.getElementById("nom").value,
        prenom: document.getElementById("prenom").value,
        age: parseFloat(document.getElementById("age").value),
        gender: parseInt(document.getElementById("sexe").value),
        poids: poids,
        dose: dose,
        c3: c3,
        dp: dp
    };

    console.log("Patient :", patientData);
});

btnRecommandation.addEventListener("click", () => {

    if (dp === null) {
        alert("Veuillez d'abord cliquer sur Calculer.");
        return;
    }

    localStorage.setItem(
        "patientData",
        JSON.stringify(patientData)
    );

    window.location.href = "recommendation.html";
});