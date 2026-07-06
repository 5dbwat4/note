import { autoContentFiles } from "#accumbens/config";
export default {
    "dir":import.meta.url,
    "path":{
        "default":false,
        "aliases":["Misc/kemu1"], 
    },
    "entries":autoContentFiles(),
    "index":"main.md",
    "name":"科目一",
    "show":true,
}