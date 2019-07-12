var editor = CodeMirror.fromTextArea(document.getElementById("question-code-area"), {
    theme: 'monokai',
    mode: 'python',
    lineNumbers: true,
    indentUnit: 4,
    lineWrapping: true,
    readOnly: true
});

editor.setSize('100%', 'auto');
