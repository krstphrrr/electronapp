

const {dialog} = require('electron').remote;
const {ipcRenderer} = require('electron')
const getbtn = document.getElementById('getbtn')
const setbtn = document.getElementById('setbtn')
const py = require('python-shell')


// setbtn.addEventListener('click', (event)=>{
//     ipcRenderer.send('open-file-dialog')
// })

// setbtn.addEventListener('click',(event)=>{
//     client.invoke("echo", "h", (err,res)=>{
//         if(err){
//             //
//         } else{
//             document.getElementById('selected-file').innerHTML = res
//         }
//     })
// })

// ipcRenderer.on('stringsignal',(event,data)=>{
//     document.getElementById('selected-file').value = data
// })

// getbtn.addEventListener('click', (event)=>{
//     document.getElementById('selected-file').innerHTML = dialog.showOpenDialogSync({properties: ['openDirectory', 'createDirectory']})
// })


