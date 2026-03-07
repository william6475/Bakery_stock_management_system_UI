function hide_block_add_record_form(is_edit_operation) {
     //Hide the form
     const form_elements = document.getElementsByClassName("add_row_form_element");
     for (let i = 0; i < form_elements.length; i++) {
        form_elements[i].style.display = "none";
        form_elements[i].style.disabled = true;

     }

    //Show the add row button
    document.getElementById("add_row_button").disabled = false;
    document.getElementById("add_row_button").style.display = "block";
}

function show_unblock_record_form(){
    //Show the form
    const form_elements = document.getElementsByClassName("add_row_form_element");
    for(let i = 0; i < form_elements.length; i++){
        form_elements[i].style.display = "";
        form_elements[i].style.disabled = false;
    }

    //Show the add row button
    document.getElementById("add_row_button").style.display = "none";
    document.getElementById("add_row_button").disabled = true;
    //Adapt the spacing for each of the column labels to align with the form fields
    const table_headings = document.getElementsByClassName("field_labels");

}