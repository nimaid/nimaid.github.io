// Constants from: https://www.unicode.org/charts/PDF/U2800.pdf
const BASE_ADDRESS = 0x2800;
const MAX_ADDRESS = 0x28FF;


// Base Functions
/**
 * Encodes binary data into braille text (Unicode).
 * 
 * @param {Uint8Array} data - The data to encode.
 * @returns {String} braille - The encoded braille text.
 */
function encodeBraille(data) {
    var braille = ""
    
    data.forEach((value, index) => {
        var codePoint = (value & 0b00000001) << 7
        codePoint |= (value & 0b00000010) << 4
        codePoint |= (value & 0b00000100) << 2
        codePoint |= value & 0b00001000
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
function decodeBraille(braille) {
    var data = new Uint8Array(braille.length)
    
    for (let i = 0; i < braille.length; i++) {
        var codePoint = braille.codePointAt(i)
        
        if ((codePoint < BASE_ADDRESS) | (codePoint > MAX_ADDRESS)) {
            throw new Error(`String contains non-braille character(s): "${braille[i]}"`)
        }
        
        codePoint -= BASE_ADDRESS
        
        data[i] |= (codePoint & 0b10000000) >>> 7
        data[i] |= (codePoint & 0b00100000) >>> 4
        data[i] |= (codePoint & 0b00010000) >>> 2
        data[i] |= codePoint & 0b00001000
        data[i] |= (codePoint & 0b01000000) >>> 2
        data[i] |= (codePoint & 0b00000100) << 3
        data[i] |= (codePoint & 0b00000010) << 5
        data[i] |= (codePoint & 0b00000001) << 7
    }
    
    return data
}


// Button Functions
/**
 * Enables or disables all buttons.
 * 
 * @param {Boolean} enable - What state to set the buttons to.
 */
function setButtonsState(enable) {
    const allButtons = document.querySelectorAll('button');

    allButtons.forEach(button => {
        button.disabled = !enable;
    });
}


document.getElementById('encodeButton').addEventListener('click', async () => {
    const textArea = document.getElementById("encodedText");
    
    const input = document.createElement('input');
    input.type = 'file';

    input.onchange = e => {
        const file = e.target.files[0];
        
        setButtonsState(false);
        textArea.value = "<"
        
        if (file.name.includes(".")) {
            const ext = file.name.slice((file.name.lastIndexOf(".") - 1 >>> 0) + 2);
            
            textArea.value += `${ext}|`
        }

        // Encode the file using the FileReader API
        const reader = new FileReader();
        reader.onloadend = () => {
            textArea.value += encodeBraille(new Uint8Array(reader.result))
            
            textArea.value += ">"
            setButtonsState(true);
        };
        reader.readAsArrayBuffer(file);
        
        /*
        const stream = file.stream();
        const reader = stream.getReader();
        
        while (true) {
            const { done, value } = await reader.read();  // Uncaught SyntaxError: await is only valid in async functions, async generators and modules
            
            if (done) break;
            
            console.log("Chunk size:", value.length)
        }
        */
    }

    input.click();
});


document.getElementById('copyButton').addEventListener('click', async () => {
    const textArea = document.getElementById("encodedText");
    const softAlert = document.getElementById("softAlert");
    
    navigator.clipboard.writeText(textArea.value)
    .then(() => {
        softAlert.style.display = "block";
        setTimeout(() => {
            softAlert.style.display = "none";
        }, 2000);
    })
    .catch(err => {
        console.error("Failed to copy: ", err);
    });
});


document.getElementById('decodeButton').addEventListener('click', async () => {
    alert("Decode!")
});
