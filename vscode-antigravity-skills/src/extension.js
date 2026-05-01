const vscode = require('vscode');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const { SkillProvider } = require('./SkillProvider');

function activate(context) {
  const skillProvider = new SkillProvider();
  
  vscode.window.registerTreeDataProvider('antigravity.skillsView', skillProvider);

  let disposableRefresh = vscode.commands.registerCommand('antigravity.refreshSkills', () => {
    skillProvider.refresh();
  });
  context.subscriptions.push(disposableRefresh);

  let disposableInsert = vscode.commands.registerCommand('antigravity.insertSkill', (filePath) => {
    if (fs.existsSync(filePath)) {
      const content = fs.readFileSync(filePath, 'utf-8');
      
      const editor = vscode.window.activeTextEditor;
      if (editor) {
        editor.edit(editBuilder => {
          editBuilder.insert(editor.selection.active, "\n" + content + "\n");
        });
        vscode.window.showInformationMessage(`Skill inserted!`);
      } else {
        vscode.workspace.openTextDocument({ content: content, language: 'markdown' }).then(doc => {
          vscode.window.showTextDocument(doc);
        });
      }
    } else {
      vscode.window.showErrorMessage('Skill file not found.');
    }
  });
  context.subscriptions.push(disposableInsert);

  let disposableSync = vscode.commands.registerCommand('antigravity.syncSkills', () => {
    const psScript = path.join(__dirname, '..', 'sync.ps1');
    
    if (!fs.existsSync(psScript)) {
      vscode.window.showErrorMessage('sync.ps1 not found in extension folder.');
      return;
    }

    vscode.window.showInformationMessage('Syncing skills... Please wait.');
    
    exec(`powershell -ExecutionPolicy Bypass -File "${psScript}"`, (error, stdout, stderr) => {
      if (error) {
        vscode.window.showErrorMessage(`Sync Failed: ${error.message}`);
        return;
      }
      vscode.window.showInformationMessage('Sync Successful!');
      skillProvider.refresh();
    });
  });
  context.subscriptions.push(disposableSync);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};
