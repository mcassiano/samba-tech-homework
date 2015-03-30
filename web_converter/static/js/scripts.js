$(document).ready(function () {
    $('#status').progress();
    $('#status').css('display', 'none');
    $('#status').css('width', '300px');
    $('#status').css('margin', '0px auto');
});

function s3_upload(){

    $('#status').css('display', 'block');

    var s3upload = new S3Upload({

        file_dom_selector: '#file',
        s3_sign_put_url: '/web_converter/sign_s3',

        onProgress: function(percent, message) {

            $('#status').progress({
                percent: percent
            });

            $('.label').html(message);
        },

        onFinishS3Put: function(url) {
            $('.label').html('Upload completo. <br>Iniciando conversão...');
        },
        onError: function(status) {
            $('#label').html('Erro ao enviar arquivo. ' + status);
        }
    });
}