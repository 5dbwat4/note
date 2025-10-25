
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from "url"


function getAllentries(dir) {
    // move around the path & subpath to get all .mdx/.md filename

    const targetDirectory = dir; 
    const results = [];
    const files = fs.readdirSync(targetDirectory);
    for (const file of files) {
        const fullPath = path.join(targetDirectory, file);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
            results.push(...getAllentries(fullPath));
        } else if (file.endsWith('.mdx') || file.endsWith('.md')) {
            results.push(fullPath);
        }
    }
    return results;
}

export default {
    "dir":import.meta.url,
    "path":"papers",
    "name":"课程笔记",
    "entries":getAllentries("./noting/Papers")
}
