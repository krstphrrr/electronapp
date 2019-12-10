// import { dialog } from "electron";
// const fs = require('fs')
const {ipcRenderer} = require('electron');
const {dialog} = require('electron').remote;

const $progressBar = document.getElementById('progressBar');
const $exportBtn = document.getElementById('exportBtn');
const $directoryInput = document.getElementById('directory');
const $portInput = document.getElementById('port');
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

function openFileDialog() {
    const {dialog} = require('electron').remote;
    dialog.showOpenDialog({properties: ['openDirectory', 'createDirectory']}, function(filePaths) {
      if (filePaths) {
        $directoryInput.value = filePaths[0];
      }
    })
  }



// function getFormData(form) {
//     const data = {};
//     const inputs = form.getElementsByTagName('input')

//     for (let i = 0; i < inputs.length; i++) {
//       if(inputs[i].type == 'text' || inputs[i].type == 'password') {
//         data[inputs[i].name] = inputs[i].value
//       } else if (inputs[i].type == 'radio' || inputs[i].type == 'checkbox') {
//         if (inputs[i].checked) {
//           data[inputs[i].name] = inputs[i].value;
//         }
//       }
//     }

//     return data;
//   }


//   function setFormData(data) {
//     const form = document.getElementsByTagName('form')[0];
//     const inputs = form.getElementsByTagName('input');
//     for (let i = 0; i < inputs.length; i++) {
//       if(inputs[i].type == 'text' || inputs[i].type == 'password') {
//         inputs[i].value = data[inputs[i].name]
//       } else if (inputs[i].type == 'radio' || inputs[i].type == 'checkbox') {
//         if (data[inputs[i].name] == inputs[i].value) {
//           inputs[i].checked = true;
//         }
//       }
//     }
//   }

// document.getElementById('setbtn').addEventListener('click',()=>{
    
// });


// function reading(filepath) {
//     fs.readdir(filepath,(err,data)=>{
//         if(err){
//             alert('error occurred reading the directory');
//             return;
//         }
//         let textArea = document.getElementById('textout');

//         textArea.value = data;
//     })
// }


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