var main = function (){
    
    
    $('.btn').click(function(){
    
        $('.result').text("");
        inputs = getFormData(".inputs");
        
        //jquery AJAX post
        var url = "http://127.0.0.1:7000/hello"
        var data = JSON.stringify(inputs) //serializes json into a string, opposite of parse
        $.post( url, data, function( data ) {
            response = data['results']['response']
            $('.result').append(response)
            });
        
    });
}

function getFormData(form){
    var json={};
    var array = $(form).serializeArray();
    $.each(array, function(){
       json[this.name]=this.value || '';
    });
    return json;
}


$(document).ready(main);