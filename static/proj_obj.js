function ajax_project_dump() {
    var projname = prompt("name your project");
    params = {
        proj_name: projname,
        proj_data: JSON.stringify(project_dump())
    };

    $.post("/storeproject", params, function() {
        alert("saved.");
    });
}

function ajax_project_load() {
    var projname = prompt("what project do you want");
    $.get("/getproject?proj_name=" + projname, function(data) {
        project_load(data);
        alert("data loaded.");
    });
}
