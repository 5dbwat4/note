
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from "url"

const targetDirectory = path.parse(fileURLToPath(import.meta.url)).dir; 
function findAccumbensFolders(rootDir) {
  const results = [];

  function scanDirectory(currentDir) {
    // let foundInCurrent = false;
    const items = fs.readdirSync(currentDir);

    // 检查当前目录是否包含accumbens.config.js
    if (items.includes('accumbens.config.js')) {
      results.push(path.relative(targetDirectory, currentDir));
    //   foundInCurrent = true;
    }

    // 递归遍历所有子目录
    for (const item of items) {
      const fullPath = path.join(currentDir, item);
      if (fs.statSync(fullPath).isDirectory()) {
        scanDirectory(fullPath);
      }
    }
  }

  try {
    scanDirectory(rootDir);
  } catch (error) {
    console.error('遍历过程中出错:', error.message);
  }

  return results;
}

const foldersWithAccumbens = findAccumbensFolders(targetDirectory).filter(Boolean).map(f=>f.replace(/\\/g,'/'));
// console.log(foldersWithAccumbens);


export default {
    "dir":import.meta.url,
    "path":"",
    "name":"课程笔记",
    "subcategories":foldersWithAccumbens,
    // [
        // ...cs,
        // ...math,
        // ...phy,
        // ...other,
    // ],
    "entries":"auto"
}
