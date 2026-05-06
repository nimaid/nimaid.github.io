import { encodeBraille, decodeBraille } from "https://raw.githubusercontent.com/nimaid/binary-cuneiform/refs/heads/main/js/braillebyte.js";


let test = new Uint8Array([1,2,3,4,253,254,255])
console.log(decodeBraille(encodeBraille(test)))
