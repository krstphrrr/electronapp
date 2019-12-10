'use strict';
const electron = require('electron')

const app = electron.app
const ipcMain = electron.ipcMain
const Menu = electron.Menu
const BrowserWindow = electron.BrowserWindow

const fs = require('fs')
const url = require('url')
const path = require('path')
// const {app, BrowserWindow} = require('electron')
// const locals = {/* ...*/}
const setupPug = require('electron-pug')

let win;
app.mainWindow = win;

const name = electron.app.name
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

////////////////////////////////
// const initApp = async function(){
//     try{
//         let pug = await setupPug({pretty:true})
//         pug.on('error', err => console.error('electron-pug error', err))
//     } catch (err){
// //
//     }
//     const menu = Menu.buildFromTemplate(template)
//     Menu.setApplicationMenu(menu)


//     let mainWindow = new BrowserWindow({
//         width:860, 
//         height:580,
//         webPreferences:{
//             nodeIntegration:true
//         }
//     })
//     mainWindow.loadURL(`file://${__dirname}/views/index.pug`)

//     mainWindow.webContents.openDevTools()

//     mainWindow.on('closed', ()=> {
//         mainWindow=null
//     })
// }
/////////////////////////////
let mainWindow

function createWindow () {
  const menu = Menu.buildFromTemplate(template)
  Menu.setApplicationMenu(menu)

  // Create the browser window.
  mainWindow = new BrowserWindow({width: 860, height: 580})

  // and load the index.html of the app.
  mainWindow.loadURL(url.format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }))

  // Open the DevTools.
  mainWindow.webContents.openDevTools()

  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null
  })
}

app.on('ready', createWindow)
app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') {
      app.quit()
    }
  })
app.on('activate', function () {

if (mainWindow === null) {
    createWindow()
  }
})

ipcMain.on('signal1',()=>{
    console.log('ok')
})
    // const {dialog} = require('electron') 
    // dialog.showOpenDialog({properties: ['openDirectory', 'createDirectory']},(foldername)=>{
    //     if(foldername === undefined){
    //         alert("no dir apparently");
    //     } else {
    //         // readFile(foldername[0]);
    //         console.log("open")
    //     }      
    // })
    // function readFile(filepath) {
    //     fs.readdir(filepath,(err, data)=>{
    //         if (err){
    //             alert('couldn\'t read dir')
    //             return
    //         }
    //         event.senderd.send('fileData', data)
    //     })
    // }
    
// })


// app.on('ready', initApp)


// // called when windows are closed
// app.on('window-all-closed', ()=> {
//     if(process.platform !=='darwin'){
//         app.quit()
//     }
// })

// app.on('activate', ()=> {
//     if (win===null){
//         initApp()
//     }
// })