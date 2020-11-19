
var hide = function(){
    // esconder os botoes todos quando clica num botao
    $("#edit-name-btn").hide();
    $("#edit-sex-btn").hide();
    $("#edit-description-btn").hide();
    $("#edit-birthdate-btn").hide();
}

$("#edit-submit").click(function(){
    // mostrar todos os botoes
})


$("#edit-name-btn").click(function(){
    $("#display-name").hide();
    $("#edit-name").show();
    hide();
    let name= $("#display-name").html().trim();
    $("#id_name").val(name);
})

$("#edit-sex-btn").click(function(){
    $("#display-sex").hide();
    $("#edit-sex").show();
    hide();
    let sex = $("#display-sex").html().trim();
    let num=1;
    if (sex=="Female"){ num = 2;}else if(sex=="Other"){ num = 3;};
    $("#id_sex").val(num);
})

$("#edit-birthdate-btn").click(function(){
    $("#display-birthdate").hide();
    $("#edit-birthdate").show();
    hide();
    /*
    let date =$("#display-birthdate").html().trim().split(".");
    console.log(date);
    let date_obj = new Date(date[1].split(",")[0]+"-"+date[0]+"-"+date[1].split(",")[1]);
    console.log(date_obj);
    $("#id_birthdate").val(date_obj);
    */

})

$("#edit-description-btn").click(function(){
    $("#display-description").hide();
    $("#edit-description").show();
    hide();
    console.log($("#display-description").html().trim());
    let description = $("#display-description").html().trim();
    $("#id_description").val(description);
})

