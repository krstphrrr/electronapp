'use strict';
const electron = require('electron')
const {app, ipcMain, dialog, Menu, BrowserWindow} = require('electron')


const url = require('url')
const path = require('path')
// const {app, BrowserWindow} = require('electron')
// const locals = {/* ...*/}
const setupPug = require('electron-pug')

let win;
app.mainWindow = win;

const name = app.name
const template = [{
    label: name,
    submenu:[{
       label: `About ${name}`,
        role: 'about'
      }]
  }, {
      label: "Edit",
      submenu: [
          { label: "Undo", accelerator: "CmdOrCtrl+Z", selector: "undo:" },
          { label: "Redo", accelerator: "Shift+CmdOrCtrl+Z", selector: "redo:" },
          { type: "separator" },
          { label: "Cut", accelerator: "CmdOrCtrl+X", selector: "cut:" },
          { label: "Copy", accelerator: "CmdOrCtrl+C", selector: "copy:" },
          { label: "Paste", accelerator: "CmdOrCtrl+V", selector: "paste:" },
          { label: "Select All", accelerator: "CmdOrCtrl+A", selector: "selectAll:" }
      ]}]


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
        width:860, 
        height:580,
        webPreferences:{
            nodeIntegration:true
        }
    })
    mainWindow.loadURL('../views/index.pug')

    // mainWindow.webContents.openDevTools()

    mainWindow.on('closed', ()=> {
        mainWindow=null
    })
}

ipcMain.on('open-file-dialog',(event)=>{
    // console.log('before dialog')
    dialog.showOpenDialog({properties: ['openDirectory']},files=>event.sender.send('selected-directory', files))
    // if (str) {
    //     event.sender.send('selected-directory', str)
    // }
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