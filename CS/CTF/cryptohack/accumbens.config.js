import { autoContentFiles } from "#accumbens/config";
export default {
    "dir":import.meta.url,
    "path":{
        "default":false,
        "aliases":["CS/CTF/Cryptohack","CTF/Cryptohack"], 
    },
    "entries":autoContentFiles(),
    "name":"Learn Cryptohack",
    "show":true,
}