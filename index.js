

const {dialog} = require('electron').remote;
const {ipcRenderer} = require('electron')
// const getbtn = document.getElementById('getbtn')
// const setbtn = document.getElementById('setbtn')
// const py = require('python-shell')


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

const setbtn = document.getElementById('setbtn')
let variable = ''

setbtn.addEventListener('click', (event)=>{
    document.getElementById('textout').innerHTML = dialog.showOpenDialogSync({properties: ['openFile']})
    variable = document.getElementById('textout').innerHTML;
    get_dimapath();
    // document.getElementById('textout').innerHTML ='',
})

function get_dimapath(){
    const {PythonShell} = require('python-shell')
    const {dialog} = require('electron').remote;
    const path = require("path")

    // const textval = document.getElementById('textin')

    const options = {
        scriptPath: './scripts/',
        pythonPath: 'C:\\Users\\kbonefont\\AppData\\Local\\Continuum\\miniconda3\\python.exe',
        args: [variable]
    }
    let pyshell = new PythonShell('dimatest.py',options)

    pyshell.on('message', (message)=>{
        document.getElementById('textout2').innerHTML = message
    }) 

    document.getElementById('outlabel').style.display = "none";
    document.getElementById('outlabel2').style.display = "none";

}
