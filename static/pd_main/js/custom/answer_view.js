var answer_code_editor = CodeMirror.fromTextArea(document.getElementById("answer-code"), {
    theme: 'monokai',
    mode: 'python',
    lineNumbers: true,
    lineWrapping: true,
    indentUnit: 4
});

var answer_explanation = CodeMirror.fromTextArea(document.getElementById("answer-explanation"), {
    mode: 'markdown'
});

answer_code_editor.setSize('100%', 'auto');
answer_explanation.setSize('100%', 'auto');

$('#submit_button').click(function () {

    // hide the submit button
    // $('#submit_button').hide();

    html2canvas(document.body).then(canvas => {

        // toDataURL defaults to png
        image_data = canvas.toDataURL();
        $('#id_image_data').val(image_data);
        $('#answer_output_form').submit();
    });
});
