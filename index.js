

const {dialog} = require('electron').remote;
const {ipcRenderer} = require('electron')
const {app, BrowserWindow} = require('electron').remote
const path = require('path')
const setupPug = require('electron-pug')
const popbtn = document.getElementById('popbtn')
const setbtn = document.getElementById('setbtn')
const pypath = process.env.pyPATH

let variable = ''

setbtn.addEventListener('click', (event)=>{
    ipcRenderer.send("processenv")
 
    document.getElementById('textout2').innerHTML=''
    variable = dialog.showOpenDialogSync({properties: ['openFile']})
    document.getElementById('textout').innerHTML = variable

    if (variable===undefined){
        document.getElementById('outlabel').style.display = "none";
        document.getElementById('outlabel2').style.display = "none";
        document.getElementById('textout2').innerHTML= 'no file chosen'
        
    } else {
        get_dimapath();
    }
})

function get_dimapath(){
    const {PythonShell} = require('python-shell')
    const {dialog} = require('electron').remote;
    const path = require("path")

    const options = {
        scriptPath: './scripts/',
        pythonPath: pypath,
        args: [variable]
    }
    let pyshell = new PythonShell('test_pk.py',options)

    pyshell.on('message', (message)=>{
        document.getElementById('textout2').innerHTML = message
    }) 

    document.getElementById('outlabel').style.display = "none";
    document.getElementById('outlabel2').style.display = "none";

}

popbtn.addEventListener('click', (event)=>{
    document.getElementById('textout1').innerHTML=''
    document.getElementById('textout2').innerHTML=''
    drop_tables()
})
function drop_tables(){
    const {PythonShell} = require('python-shell')
    const {dialog} = require('electron').remote;
    const path = require("path")

    const options = {
        scriptPath: './scripts/',
        pythonPath: pypath,
        args: [variable]
    }
    let pyshell = new PythonShell('dropper.py',options)

    pyshell.on('message', (message)=>{
        document.getElementById('textout2').innerHTML = message
    }) 

    document.getElementById('outlabel').style.display = "none";
    document.getElementById('outlabel2').style.display = "none";
}