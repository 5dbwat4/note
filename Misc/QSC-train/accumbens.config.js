import { autoContentFiles } from "#accumbens/config";
export default {
    "dir":import.meta.url,
    "path":{
        "default":false,
        "aliases":["Misc/QSC-train"], 
    },
    "entries":autoContentFiles(),
    "name":"QSC内训",
    "show":true,
}