import { autoContentFiles } from "#accumbens/config";
export default {
    "dir":import.meta.url,
    "path":{
        "default":false,
        "aliases":["Schoolwork/CS1030M","CS/CS1030M","CS/HPC101"], 
    },
    "entries":autoContentFiles(),
    "name":"HPC101",
    "show":true,
}