

const {dialog} = require('electron').remote;
const {ipcRenderer} = require('electron')
const {app, BrowserWindow} = require('electron').remote
const path = require('path')
const setupPug = require('electron-pug')
const popbtn = document.getElementById('popbtn')
const setbtn = document.getElementById('setbtn')
const pypath = process.env.pyPATH

// button that opens dialog and chooses dima file
let variable = ''

setbtn.addEventListener('click', (event)=>{
    // ipcRenderer.send("processenv")
 
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
        pythonPath: 'C:\\Users\\kbonefont\\AppData\\Local\\Continuum\\miniconda3\\python.exe',
        args: [variable]
    }
    let pyshell = new PythonShell('test_pk.py',options)

    pyshell.on('message', (message)=>{
        document.getElementById('textout2').innerHTML = message
    }) 

    document.getElementById('outlabel').style.display = "none";
    document.getElementById('outlabel2').style.display = "none";

}


// button that drops all tables
// process should happen in invisible window
popbtn.addEventListener('click', (event)=>{
    // document.getElementById('textout1').innerHTML=''
    // document.getElementById('textout2').innerHTML=''
    // drop_tables()
    const windowID = BrowserWindow.getFocusedWindow().id
    const invisPath = path.join(path.dirname(__dirname),'/public/pop.html')
    let win = new BrowserWindow({
        width:400,
        height:400,
        show:true,
        webPreferences: {
            nodeIntegration: true
        }
    })
    win.loadURL(invisPath)
    win.webContents.openDevTools()

    win.webContents.on('did-finish-load', ()=>{
        win.webContents.send('dostuff', windowID)
    })

})
ipcRenderer.on('pop',(event, output)=>{
    document.getElementById('textout2').innerHTML = "lo"
})
// ipcRenderer.on('stuffdone',(event,output)=>{

//     // disabler(output)
//     // const res = `${output}`
//     document.getElementById('outlabel').style.display = "none";
//     document.getElementById('outlabel2').style.display = "none";
//     document.getElementById('textout2').innerHTML = `${output}`
// })

// function disabler(output){
//     document.getElementById('popbtn').disabled = true
//     document.getElementById('textout2').innerHTML = `${output}`

// }
// ipcRenderer.on('stuffdone', (event)=>{
//     // const message = `dropping of ${output} done`
//     document.getElementById('outlabel').style.display = "none";
//     document.getElementById('outlabel2').style.display = "none";
//     document.getElementById('textout2').innerHTML = "tables dropped"

// })

// function drop_tables(){
//     const {PythonShell} = require('python-shell')
//     const path = require("path")

//     const options = {
//         scriptPath: './scripts/',
//         pythonPath: 'C:\\Users\\kbonefont\\AppData\\Local\\Continuum\\miniconda3\\python.exe',
//         args: [variable]
//     }
//     let pyshell = new PythonShell('dropper.py',options)

//     pyshell.on('message', (message)=>{
//         document.getElementById('textout2').innerHTML = message
//     }) 

//     document.getElementById('outlabel').style.display = "none";
//     document.getElementById('outlabel2').style.display = "none";
// }