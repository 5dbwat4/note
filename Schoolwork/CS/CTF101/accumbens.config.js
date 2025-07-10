import fs from "fs";
import { fileURLToPath } from "url";

export default {
    "dir":import.meta.url,
    "path":{
        "default":true,
    },
    "entries":await fs.promises.readdir(fileURLToPath(importPath)).filter(e=>!e.endsWith(".protected.mdx")),
    "name":"CTF101",
    "show":false,
}