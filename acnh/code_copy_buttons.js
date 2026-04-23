document.querySelectorAll('pre').forEach(preBlock => {
    // Create the button
    const btn = document.createElement('button');
    btn.className = 'copy-button';
    btn.textContent = 'Copy';
    btn.style.position = 'absolute';
    btn.style.top = '1px';
    btn.style.right = '1px';
    
    // Position the parent pre block
    preBlock.style.position = 'relative';
    preBlock.appendChild(btn);
    
    // Copy functionality
    btn.onclick = () => {
        const code = preBlock.querySelector('code');
        const text = code ? code.innerText : preBlock.innerText;
        navigator.clipboard.writeText(text).then(() => {
            btn.textContent = 'Copied!';
            setTimeout(() => btn.textContent = 'Copy', 2000);
        });
    };
});
