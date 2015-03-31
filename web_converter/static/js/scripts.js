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

            $.get("/web_converter/add_job", {s3_input_file: url}).done(function(data) {

                data = $.parseJSON(data);
                
                var job_id = data.id;
                var output_url = data.outputs[0].url;

                $('#status').progress({
                    percent: 0
                });

                setInterval(function() {

                    $.get("/web_converter/get_status_on_job",
                        {zencoder_job_id: job_id}).done(function(data) {

                            data = $.parseJSON(data);

                            $('.label').html(data.state);


                            $('#status').progress({
                                percent: data.progress
                            });

                            if (data.state == "finished")
                                clearInterval();
                    });

                }, 1000);

                $('.label').html('Vídeo em ' + output_url);

            });



        },
        onError: function(status) {
            $('#label').html('Erro ao enviar arquivo. ' + status);
        }
    });
}