function deleteConfirm(){

return confirm("Are you sure you want to delete this task?");

}

function completeTask(){

alert("Task marked as Completed!");

}

function validateForm(){

let title=document.getElementById("title").value;

if(title==""){

alert("Task title is required");

return false;

}

return true;

}
