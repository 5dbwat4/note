import { autoContentFiles } from "#accumbens/config";

export default {
    "dir":import.meta.url,
    "path":{
        "default":true,
    },
    "entries":autoContentFiles(),
    "name":"example",
    "show":false,
}