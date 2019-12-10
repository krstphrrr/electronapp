

const {dialog} = require('electron').remote;

const $progressBar = document.getElementById('progressBar');
const $exportBtn = document.getElementById('exportBtn');
const $directoryInput = document.getElementById('directory');


export function openFileDialog() {
    const {dialog} = require('electron').remote;
    dialog.showOpenDialog({properties: ['openDirectory', 'createDirectory']}, function(filePaths) {
      if (filePaths) {
        $directoryInput.value = filePaths[0];
      }
    })
  }



