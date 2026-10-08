const patientData =
    JSON.parse(localStorage.getItem("patientData"));


if (!patientData) {

    alert("Aucune donnée patient trouvée.");

    window.location.href = "index.html";

} else {

    document.getElementById("patientName").textContent =
        `${patientData.nom} ${patientData.prenom}`;

    document.getElementById("patientWeight").textContent =
        patientData.poids + " kg";

    document.getElementById("currentDose").textContent =
        patientData.dose + " mg/j";

    document.getElementById("patientC3").textContent =
        patientData.c3 + " mg/L";
}


/*
 * Bouton PRÉDIRE
 */
document.getElementById("btnPredire")
    .addEventListener("click", async () => {

        try {

            const dpC1 =
                patientData.dp / patientData.c3;

            const result =
                await window.electronAPI.predict({

                    dp_c1: dpC1,

                    gender: patientData.gender,

                    weight: patientData.poids

                });


            if (!result.success) {

                throw new Error(result.error);

            }


            /*
             * Affichage DP/C2
             */

            document.getElementById("dpC2Result")
                .textContent =
                result.dp_c2.toFixed(4);


            /*
             * Affichage des doses
             */

            document.getElementById("doseMin")
                .textContent =
                result.dose_min.toFixed(2);

            document.getElementById("doseAverage")
                .textContent =
                result.dose_average.toFixed(2);

            document.getElementById("doseMax")
                .textContent =
                result.dose_max.toFixed(2);


            /*
             * Stocker les résultats
             * pour l'enregistrement
             */

            patientData.dp_c2_pred =
                result.dp_c2;

            patientData.dose_min =
                result.dose_min;

            patientData.dose_average =
                result.dose_average;

            patientData.dose_max =
                result.dose_max;


            /*
             * Afficher la zone de résultats
             */

            document.getElementById("predictionResults")
                .classList.remove("hidden");


        } catch (error) {

            console.error(error);

            alert(
                "Erreur lors de la prédiction :\n" +
                error.message
            );

        }

    });


/*
 * Bouton RETOUR
 */
document.getElementById("btnRetour")
    .addEventListener("click", () => {

        window.location.href = "index.html";

    });


/*
 * Bouton ENREGISTRER
 */
document.getElementById("btnEnregistrer")
    .addEventListener("click", async () => {

        try {

            const result =
                await window.electronAPI.savePatient(
                    patientData
                );


            if (!result.success) {

                throw new Error(result.error);

            }


            document.getElementById("successMessage")
                .classList.remove("hidden");


            document.getElementById("btnEnregistrer")
                .disabled = true;


        } catch (error) {

            console.error(error);

            alert(
                "Erreur lors de l'enregistrement :\n" +
                error.message
            );

        }

    });