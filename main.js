'use strict';
const { app, ipcMain, Menu, BrowserWindow }= require('electron')
const pug = require('pug')


const url = require('url')
const path = require('path')
// const {app, BrowserWindow} = require('electron')
// const locals = {/* ...*/}
const ElectronViewRenderer = require('electron-view-renderer')
const viewRenderer = new ElectronViewRenderer({
    viewPath: 'views',            // default 'views'
    viewProtcolName: 'view',      // default 'view'
    useAssets: true,               // default false
    assetsPath: 'assets',          // default 'assets'
    assetsProtocolName: 'asset'   // default 'asset'
})

viewRenderer.add('pug', {
  extension: '.pug',
  viewPath: 'views',
  rendererAction: (filePath, viewData, callback) => {
    pug.renderFile(filePath, viewData, (error, html) => {
      if (error) {
        if (error.file) error.message += `\n\nERROR @(${error.file}:${error.line}:${error.column})`
        throw new Error(error)
      }

      callback(html)
    })
  }
})

viewRenderer.use('pug')

let mainWindow

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 860,
        height: 580,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    })

    // NOTE: instead of loading a url as the Quick Start example shows, we are
    //       going to use the viewRenderer helper
    // const viewOptions = { name: "Bob" }
    viewRenderer.load(mainWindow, 'index')

    // mainWindow.webContents.openDevTools()
    mainWindow.on('closed', () => { mainWindow = null })
}

app.on('ready', createWindow)
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit() })
app.on('activate', () => { if (mainWindow === null) createWindow() })


// let win;
// app.mainWindow = win;

// let mainWindow;

// const name = app.name
// const template = [{
//     label: name,
//     submenu:[{
//        label: `About ${name}`,
//         role: 'about'
//       }]
//   }, {
//       label: "Edit",
//       submenu: [
//           { label: "Undo", accelerator: "CmdOrCtrl+Z", selector: "undo:" },
//           { label: "Redo", accelerator: "Shift+CmdOrCtrl+Z", selector: "redo:" },
//           { type: "separator" },
//           { label: "Cut", accelerator: "CmdOrCtrl+X", selector: "cut:" },
//           { label: "Copy", accelerator: "CmdOrCtrl+C", selector: "copy:" },
//           { label: "Paste", accelerator: "CmdOrCtrl+V", selector: "paste:" },
//           { label: "Select All", accelerator: "CmdOrCtrl+A", selector: "selectAll:" }
//       ]}]


// app.on('ready',async () =>{
//     try{
//         let pug = await setupPug({pretty:true})
//         pug.on('error', err => console.error('electron-pug error', err))
//     } catch (err){
// //
//     }
//     // const menu = Menu.buildFromTemplate(template)
//     // Menu.setApplicationMenu(menu)


//     let mainWindow = new BrowserWindow({
//         width:860, 
//         height:580,
//         // webPreferences:{
//         //     nodeIntegration:true
//         // }
//     })
//     mainWindow.loadURL(`file://${__dirname}/views/index.pug`)

//     // mainWindow.webContents.openDevTools()

//     mainWindow.on('closed', ()=> {
//         mainWindow=null
//     })
//     mainWindow.on('ready',)
// })

// // ipcMain.on('signal1',(event,dir)=>{
// //     // async goodness: que quiero que ocurra?? aqui es donde va!
// //     console.log(dir)
// //     // mainWindow.
    
// // })


// // app.on('ready', initApp)


// // called when windows are closed
// // app.on('window-all-closed', ()=> {
// //     if(process.platform !=='darwin'){
// //         app.quit()
// //     }
// // })

// // app.on('activate', ()=> {
// //     if (win===null){
// //         initApp()
// //     }
// // })