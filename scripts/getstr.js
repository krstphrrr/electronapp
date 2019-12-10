function get_str(){
    const {PythonShell} = require('python-shell')
    const path = require("path")
    const textval = document.getElementById('textin')
    
    // const spanout = document.getElementById('textout')

    const options = {
        scriptPath: './scripts/',
        pythonPath: 'C:\\Users\\kbonefont\\AppData\\Local\\Continuum\\miniconda3\\python.exe',
        args: [textval.value]
    }
    let pyshell = new PythonShell('init.py',options)

    pyshell.on('message', (message)=>{
        document.getElementById('textout').innerHTML = message
    }) 
    document.getElementById('textin').value =""
    document.getElementById('outlabel').style.display = "none";
}

function no_str(){
    const {PythonShell} = require('python-shell')
    const path = require("path")
    const textval = document.getElementById('textin')
    
    // const spanout = document.getElementById('textout')

    const options = {
        scriptPath: './scripts/',
        pythonPath: 'C:\\Users\\kbonefont\\AppData\\Local\\Continuum\\miniconda3\\python.exe',
        args: [textval.value]
    }
    let pyshell = new PythonShell('out.py',options)

    pyshell.on('message', (message)=>{
        document.getElementById('textout').innerHTML = message
    }) 
    document.getElementById('textin').value =""
    document.getElementById('outlabel').style.display = "none";

}

function get_dimapath(){
    const {PythonShell} = require('python-shell')
    const {dialog} = require('electron').remote;
    const path = require("path")


    setbtn.addEventListener('click', (event)=>{
        document.getElementById('textout').innerHTML = dialog.showOpenDialogSync({properties: ['openDirectory', 'createDirectory']})
    })


    // const textval = document.getElementById('textin')

    // const options = {
    //     scriptPath: './scripts/',
    //     pythonPath: 'C:\\Users\\kbonefont\\AppData\\Local\\Continuum\\miniconda3\\python.exe',
    //     args: [textval.value]
    // }
    // let pyshell = new PythonShell('init.py',options)

    // pyshell.on('message', (message)=>{
    //     document.getElementById('textout').innerHTML = message
    // }) 

    // document.getElementById('textin').value =""

    

}