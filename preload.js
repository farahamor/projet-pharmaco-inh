const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {

    predict: (data) => {

        return ipcRenderer.invoke(
            "predict-inh",
            data
        );

    },

    savePatient: (data) => {

        return ipcRenderer.invoke(
            "save-patient",
            data
        );

    }

});