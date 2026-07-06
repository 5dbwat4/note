import { autoContentFiles } from "#accumbens/config";
export default {
    "dir":import.meta.url,
    "path":{
        "default":false,
        "aliases":["Schoolwork/CS1018F","CS/CS1018F","CS/FDS"], 
    },
    "entries":autoContentFiles(),
    "name":"数据结构基础",
    "show":true,
}