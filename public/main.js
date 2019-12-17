'use strict';
const electron = require('electron')
const {app, ipcMain, dialog, Menu, BrowserWindow} = require('electron')


const url = require('url')
const path = require('path')

const setupPug = require('electron-pug')

let win;
app.mainWindow = win;

const basedir = app.getPath('home')
console.log(basedir)
const name = app.name
const template = [{
    label: name,
    submenu:[{
       label: `About ${name}`,
        role: 'about'
      }]
  }]


const initApp = async function(){
    try{
        let pug = await setupPug({pretty:true})
        pug.on('error', err => console.error('electron-pug error', err))
    } catch (err){
//
    }
    const menu = Menu.buildFromTemplate(template)
    Menu.setApplicationMenu(menu)


    let mainWindow = new BrowserWindow({
        width:600, 
        height:350,
        resizable: false,
        // frame:false,
        webPreferences:{
            nodeIntegration:true
        }
    })
    mainWindow.loadURL(path.join(path.dirname(__dirname),'/views/index.pug'))

    // mainWindow.webContents.openDevTools()

    mainWindow.on('closed', ()=> {
        mainWindow=null
    })
}

ipcMain.on('pop',(event, output)=>{
    console.log(`${output}`)
})


app.on('ready', initApp)


// called when windows are closed
app.on('window-all-closed', ()=> {
    if(process.platform !=='darwin'){
        app.quit()
    }
})

app.on('activate', ()=> {
    if (win===null){
        initApp()
    }
})