// Constants from: https://www.unicode.org/charts/PDF/U2800.pdf
const BASE_ADDRESS = 0x2800;
const MAX_ADDRESS = 0x28FF;


/**
 * Encodes binary data into braille text (Unicode).
 * 
 * @param {Uint8Array} data - The data to encode.
 * @returns {String} braille - The encoded braille text.
 */
export function encodeBraille(data) {
    var braille = ""
    
    data.forEach((value, index) => {
        var codePoint = (value & 0b00000001) << 7
        codePoint |= (value & 0b00000010) << 4
        codePoint |= (value & 0b00000100) << 2
        codePoint |= (value & 0b00001000)
        codePoint |= (value & 0b00010000) << 2
        codePoint |= (value & 0b00100000) >>> 3
        codePoint |= (value & 0b01000000) >>> 5
        codePoint |= (value & 0b10000000) >>> 7
        
        codePoint += BASE_ADDRESS
        
        braille += String.fromCodePoint(codePoint)
    });
    
    return braille
}


/**
 * Decodes braille text (Unicode) into binary data.
 * 
 * @param {String} braille - The braille text to decode.
 * @returns {Uint8Array} data - The decoded data.
 */
export function decodeBraille(braille) {
    var data = new Uint8Array(braille.length)
    
    for (let i = 0; i < braille.length; i++) {
        var codePoint = braille.codePointAt(i)
        
        if ((codePoint < BASE_ADDRESS) | (codePoint > 0x28FF)) {
            throw new Error(`String contains non-braille character(s): "${braille[i]}"`)
        }
        
        codePoint -= BASE_ADDRESS
        
        data[i] |= (codePoint & 0b10000000) >>> 7
        data[i] |= (codePoint & 0b00100000) >>> 4
        data[i] |= (codePoint & 0b00010000) >>> 2
        data[i] |= (codePoint & 0b00001000)
        data[i] |= (codePoint & 0b01000000) >>> 2
        data[i] |= (codePoint & 0b00000100) << 3
        data[i] |= (codePoint & 0b00000010) << 5
        data[i] |= (codePoint & 0b00000001) << 7
    }
    
    return data
}
