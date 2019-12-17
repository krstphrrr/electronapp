

const {dialog} = require('electron').remote;
const {ipcRenderer} = require('electron')
const {app, BrowserWindow} = require('electron').remote
const path = require('path')
const setupPug = require('electron-pug')
const popbtn = document.getElementById('popbtn')
const setbtn = document.getElementById('setbtn')
const txtout1 = document.getElementById('textout')
const txtout2 = document.getElementById('textout2')
const lbl1 = document.getElementById('outlabel')
const lbl2 = document.getElementById('outlabel2')
const pypath = process.env.pyPATH

// button that opens dialog and chooses dima file
let variable = ''

setbtn.addEventListener('click', (event)=>{
    // ipcRenderer.send("processenv")
 
    txtout2.innerHTML=''
    variable = dialog.showOpenDialogSync({properties: ['openFile']})
    txtout1.innerHTML = variable

    if (variable===undefined){
        lbl1.style.display = "none";
        lbl2.style.display = "none";
        txtout2.innerHTML= 'no file chosen'
        
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
        pythonPath: 'C:\\Users\\kbonefont\\AppData\\Local\\Continuum\\miniconda3\\python.exe',
        args: [variable]
    }
    let pyshell = new PythonShell('test_pk.py',options)

    pyshell.on('message', (message)=>{
        txtout2.innerHTML = message
    }) 

    lbl1.style.display = "none";
    lbl2.style.display = "none";

}


// button that drops all tables
// process should happen in invisible window
popbtn.addEventListener('click', (event)=>{

    const windowID = BrowserWindow.getFocusedWindow().id
    const invisPath = path.join(path.dirname(__dirname),'/public/droptables.html')
    let win = new BrowserWindow({
        width:400,
        height:400,
        show:false,
        webPreferences: {
            nodeIntegration: true
        }
    })
    win.loadURL(invisPath)
    // win.webContents.openDevTools()

    win.webContents.on('did-finish-load', ()=>{
        win.webContents.send('dostuff', windowID)
    })

})

ipcRenderer.on('stuffdone',(event)=>{
    // const res = `${output}`
    lbl1.style.display = "none";
    lbl2.style.display = "none";
    txtout1.innerHTML = ""
    txtout2.innerHTML = "tables dropped"
})