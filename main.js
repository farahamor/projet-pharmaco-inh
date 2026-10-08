const {
    app,
    BrowserWindow,
    ipcMain
} = require("electron");

const path = require("path");
const { spawn } = require("child_process");


function createWindow() {

    const win = new BrowserWindow({
        width: 1200,
        height: 800,

        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            contextIsolation: true,
            nodeIntegration: false
        }
    });

    win.loadFile(
        path.join(__dirname, "frontend", "index.html")
    );
}


/* ================================
   PRÉDICTION PYTHON
   ================================ */

ipcMain.handle("predict-inh", async (event, data) => {

    return new Promise((resolve, reject) => {

        const python = spawn(
            "python",
            [
                path.join(
                    __dirname,
                    "backend",
                    "predict_cli.py"
                )
            ],
            {
                cwd: path.join(__dirname, "backend")
            }
        );

        let output = "";
        let errorOutput = "";

        python.stdout.on("data", (data) => {
            output += data.toString();
        });

        python.stderr.on("data", (data) => {
            errorOutput += data.toString();
        });

        python.on("close", (code) => {

            if (code !== 0) {

                reject(
                    new Error(
                        errorOutput ||
                        "Erreur lors de l'exécution de Python"
                    )
                );

                return;
            }

            try {

                const result = JSON.parse(output);

                resolve(result);

            } catch (error) {

                reject(
                    new Error(
                        "Réponse Python invalide : " +
                        output
                    )
                );
            }
        });

        python.stdin.write(
            JSON.stringify(data)
        );

        python.stdin.end();

    });

});


/* ================================
   ENREGISTREMENT DU PATIENT
   ================================ */

ipcMain.handle("save-patient", async (event, data) => {

    return new Promise((resolve, reject) => {

        const python = spawn(
            "python",
            [
                path.join(
                    __dirname,
                    "backend",
                    "save_patient_cli.py"
                )
            ],
            {
                cwd: path.join(__dirname, "backend")
            }
        );

        let output = "";
        let errorOutput = "";

        python.stdout.on("data", (data) => {
            output += data.toString();
        });

        python.stderr.on("data", (data) => {
            errorOutput += data.toString();
        });

        python.on("close", (code) => {

            if (code !== 0) {

                reject(
                    new Error(
                        errorOutput ||
                        "Erreur lors de l'enregistrement"
                    )
                );

                return;
            }

            try {

                const result = JSON.parse(output);

                resolve(result);

            } catch (error) {

                reject(
                    new Error(
                        "Réponse Python invalide : " +
                        output
                    )
                );
            }

        });

        python.stdin.write(
            JSON.stringify(data)
        );

        python.stdin.end();

    });

});


/* ================================
   DÉMARRAGE ELECTRON
   ================================ */

app.whenReady().then(() => {

    createWindow();

    app.on("activate", () => {

        if (
            BrowserWindow.getAllWindows().length === 0
        ) {
            createWindow();
        }

    });

});


app.on("window-all-closed", () => {

    if (process.platform !== "darwin") {
        app.quit();
    }

});