// import { dialog } from "electron";
const fs = require('fs')
const {ipcRenderer} = require('electron')
const {dialog} = require('electron').remote;
// const $directoryInput = document.getElementById('directory');
// const $portInput = document.getElementById('port');
// const $textOut = document.getElementById('textout')

// function openFileDialog(){
//     dialog.showOpenDialog({properties: ['openDirectory', 'createDirectory']}, function(filePaths){
//         if (filePaths){
//             $textOut.value = filePaths[0]

//         }
//     })
// }

// document.getElementById('setbtn').addEventListener('click', function (event) {
//     dialog.showOpenDialog({
//         properties: ['openDirectory', 'createDirectory']
//     }, function (files) {
//         if (files !== undefined) {
//             ipcRenderer('signal1', files[0])
//         }
//     });
// });


document.getElementById('setbtn').onclick = () => {
    dialog.showOpenDialog({properties: ['openDirectory', 'createDirectory']},(foldername)=>{
        if(foldername === undefined){
            alert("no dir apparently");
        } else {
            reading(foldername[0]);
        }      
    })
}


function reading(filepath) {
    fs.readdir(filepath,(err,data)=>{
        if(err){
            alert('error occurred reading the directory');
            return;
        }
        let textArea = document.getElementById('textout');

        textArea.value = data;
    })
}


// document.getElementById('setbtn').addEventListener('click', ()=>{
//     dialog.showOpenDialog({properties: ['openDirectory', 'createDirectory']},(filePaths)=>{
//         document.getElementById("textout").value = filePaths[0]
//     })
        
//         // 
//         // console.log(filePaths)
        

//     // 
//     // input.value = ''
//     // })
// })

// document.getElementById('directory').addEvent