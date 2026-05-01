const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

class SkillProvider {
  constructor() {
    this._onDidChangeTreeData = new vscode.EventEmitter();
    this.onDidChangeTreeData = this._onDidChangeTreeData.event;
    // When placed in extensions folder, the structure is usually:
    // .vscode/extensions/antigravity-skills/src/SkillProvider.js
    // Let's assume skills_index.json is copied to the extension root.
    this.indexFile = path.join(__dirname, '..', 'skills_index.json');
  }

  refresh() {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element) {
    return element;
  }

  getChildren(element) {
    if (!fs.existsSync(this.indexFile)) {
      vscode.window.showInformationMessage('No skills_index.json found. Please copy it to the extension folder.');
      return Promise.resolve([]);
    }

    const data = JSON.parse(fs.readFileSync(this.indexFile, 'utf-8'));

    if (element) {
      const skillsInCategory = data.filter(s => s.category === element.label);
      return Promise.resolve(skillsInCategory.map(s => {
        const fullPath = path.join(__dirname, '..', s.path);
        return new SkillItem(s.name, vscode.TreeItemCollapsibleState.None, fullPath, s.description);
      }));
    } else {
      const categories = [...new Set(data.map(s => s.category))];
      return Promise.resolve(categories.map(c => new SkillItem(c, vscode.TreeItemCollapsibleState.Collapsed, '')));
    }
  }
}

class SkillItem extends vscode.TreeItem {
  constructor(label, collapsibleState, filePath, tooltipString) {
    super(label, collapsibleState);
    this.filePath = filePath;
    this.tooltip = tooltipString || label;
    
    if (collapsibleState === vscode.TreeItemCollapsibleState.None) {
      this.command = {
        command: 'antigravity.insertSkill',
        title: 'Insert Skill',
        arguments: [this.filePath]
      };
      this.iconPath = new vscode.ThemeIcon('markdown');
    } else {
      this.iconPath = new vscode.ThemeIcon('folder');
    }
  }
}

module.exports = { SkillProvider, SkillItem };
