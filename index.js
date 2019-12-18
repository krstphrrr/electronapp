

const {dialog} = require('electron').remote;
const {ipcRenderer} = require('electron')
const {app, BrowserWindow} = require('electron').remote
const path = require('path')
const setupPug = require('electron-pug')
// const popbtn = document.getElementById('popbtn')
// const setbtn = document.getElementById('setbtn')
// const txtout1 = document.getElementById('textout')
// const txtout2 = document.getElementById('textout2')
// const lbl1 = document.getElementById('outlabel')
// const lbl2 = document.getElementById('outlabel2')
const pypath = process.env.pyPATH

// button that opens dialog and chooses dima file
let variable = ''

$('#setbtn').on('click', (event)=>{
    // ipcRenderer.send("processenv")
 
    $('#textout2').innerHTML=''
    variable = dialog.showOpenDialogSync({properties: ['openFile']})
    $('#textout').innerHTML = variable

    if (variable===undefined){
        $('#outlabel').css('display','none');
        $('#outlabel2').css('display','none');
        $('#textout2').html('no file chosen')
        
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
       $('textout2').html(message)
    })
    // pyshell.end(function (err) {
    //     if (err) {
    //     txtout2.innerHTML = err;
    //     }
    // });
    // python_process = pyshell.childProcess;
    // python_process.kill('SIGINT'); 
    // GET THE KILL PROCESS AFTER THE FUNCTION IS EXECUTED
    // but not within the function

    $('outlabel').css('display','none')
    $('outlabel2').css('display','none')

}


// button that drops all tables
// process should happen in invisible window
$('#popbtn').on('click', (event)=>{

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
    $('outlabel').css("display", "none")
    $('outlabel2').css("display", "none")
    $('textout').html("")
    $('textout2').html("tables dropped")
})