
var hide = function(){
    // esconder os botoes todos quando clica num botao
    $("#edit-name-btn").hide();
    $("#edit-sex-btn").hide();
}

$("#edit-submit").click(function(){
    // mostrar todos os botoes
})


$("#edit-name-btn").click(function(){
    $("#display-name").hide();
    $("#edit-name").show();
    hide();
})

$("#edit-sex-btn").click(function(){
    $("#display-sex").hide();
    $("#edit-sex").show();
    hide();
})
