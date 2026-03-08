
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from "url"

const root = "./noting/Papers/";
function getAllentries(dir) {
    // move around the path & subpath to get all .mdx/.md filename

    const targetDirectory = path.join(root, dir);
    const results = [];
    const files = fs.readdirSync(targetDirectory);
    for (const file of files) {
        const fullPath = path.join(targetDirectory, file);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
            results.push(...getAllentries(path.join(dir, file)));
        } else if (file.endsWith('.mdx') || file.endsWith('.md')) {
            results.push(path.join(dir, file));
        }
    }
    return results;
}

export default {
    "dir":import.meta.url,
    "path":"papers",
    "name":"读论文",
    "entries":getAllentries("")
}
