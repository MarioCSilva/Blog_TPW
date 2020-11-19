
$("#edit_button").click(function(){

    let description = $("#display_description").html().trim();
    $("#id_description").val(description);
    $("#display_description").hide();

    $("#display_birthdate").hide();

    let sex = $("#display_sex").val();
    let num = 1;
    if(sex=="Female"){num=2;}else if(sex=="Other"){num=3;};
    $("#id_sex").val(num);
    $("#display_sex").hide();

    let name = $("#display_name").html().trim();
    $("#id_name").val(name);
    $("#display_name").hide();


    $(".edit_input").show();
    $("#edit_button").hide();




})


