document.querySelectorAll('pre').forEach(preBlock => {
    // Create the button
    const btn = document.createElement('button');
    btn.className = 'copy-button';
    btn.textContent = '';
    btn.style.background = 'transparent';
    btn.style.position = 'absolute';
    btn.style.top = '0px';
    btn.style.right = '0px';
    
    // Position the parent pre block
    preBlock.style.position = 'relative';
    preBlock.appendChild(btn);
    
    // Copy functionality
    btn.onclick = () => {
        const code = preBlock.querySelector('code');
        const text = code ? code.innerText : preBlock.innerText;
        navigator.clipboard.writeText(text).then(() => {
            btn.textContent = 'Copied!';
            btn.style.background = 'rgba(255, 255, 255, 0.9)';
            setTimeout(() => {
                btn.textContent = ''
                btn.style.background = 'transparent';
            }, 2000);
        });
    };
});
