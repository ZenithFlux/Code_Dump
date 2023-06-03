"use strict";

var jpdbBaseURL="http://api.login2explore.com:5577";
var jpdbIRL = "/api/irl";
var jpdbIML = "/api/iml";
var empDBName = "COLLAGE-DB";
var empRelationName = "PROJECT-TABLE";
var connToken = "Paste your connection token here"

$("#id").focus();

function saveRecNo2LS(jsonObj) { 
    var lvData = JSON.parse(jsonObj.data); 
    localStorage.setItem("recno", lvData.rec_no);
}

function getEmpIdAsJsonObj() {
    var id = $("#id").val(); 
    var jsonStr = {id: id};
    return JSON.stringify(jsonStr);
}

function fillData(jsonObj) {
    saveRecNo2LS(jsonObj);
    var data = JSON.parse(jsonObj.data).record;
    $("#prjname").val(data.name);
    $("#asnto").val(data.assigned_to);
    $("#asndate").val(data.assign_date);
    $("#dl").val(data.deadline);
}

function resetForm() {
    $("#id").val("");
    $("#prjname").val("");
    $("#asnto").val("");
    $("#asndate").val("");
    $("#dl").val("");

    $("#id").prop("disabled", false);
    $(".prjinfo").prop("disabled", true);
    $("#save").prop("disabled", true);
    $("#update").prop("disabled", true);
    $("#remove").prop("disabled", true);
    $("#reset").prop("disabled", true);
    $("#id").focus();
}

function removeData(){
    let removeRequest = createREMOVERecordRequest(connToken, empDBName, empRelationName, localStorage.getItem("recno"));
    jQuery.ajaxSetup({async: false});
    var resJsonObj = executeCommandAtGivenBaseUrl(removeRequest, jpdbBaseURL, jpdbIML);
    jQuery.ajaxSetup({async: true});
    resetForm();
    $("#id").focus();
}

function saveData(){
    var jsonStrObj = validateData();
    if (jsonStrObj ===''){
        return '';
    }
    var putRequest = createPUTRequest(connToken, jsonStrObj, empDBName, empRelationName);
    jQuery.ajaxSetup({async: false});
    var resJsonObj = executeCommandAtGivenBaseUrl(putRequest, jpdbBaseURL, jpdbIML);
    jQuery.ajaxSetup({async: true});
    resetForm();
    $("#id").focus();
}

function updateData() {
    var jsonChg = validateData();
    var updateRequest = createUPDATERecordRequest(connToken, jsonChg, empDBName, empRelationName, localStorage.getItem("recno"));
    jQuery.ajaxSetup({async: false});
    var resJsonObj = executeCommandAtGivenBaseUrl(updateRequest, jpdbBaseURL, jpdbIML);
    jQuery.ajaxSetup({async: true});
    console.log(resJsonObj);
    resetForm();
    $("#id").focus();
}

function getEmp() {
    var empIdJsonObj = getEmpIdAsJsonObj();
    var getRequest = createGET_BY_KEYRequest(connToken, empDBName, empRelationName, empIdJsonObj);
    jQuery.ajaxSetup({async: false});
    var resJsonObj = executeCommandAtGivenBaseUrl(getRequest, jpdbBaseURL, jpdbIRL);
    jQuery.ajaxSetup({async: true});
    if (resJsonObj.status === 400) {
        $("#save").prop("disabled", false);
    } 
    else if (resJsonObj.status === 200) {
        $( "#id").prop("disabled", true); 
        fillData(resJsonObj);
        $("#save").prop("disabled", true); 
        $("#update").prop("disabled", false); 
        $("#remove").prop("disabled", false);
    }
    $("#reset").prop("disabled", false);
    $(".prjinfo").prop("disabled", false);
    $("#prjname").focus();
}

function validateData() {
    var id, prjname, asnto, asndate, dl;
    id = $('#id').val();
    prjname = $("#prjname").val();
    asnto = $( "#asnto").val();
    asndate = $('#asndate').val();
    dl = $("#dl").val();

    if (id === ''){
        alert("Project ID missing");
        $("#id").focus();
        return "";
    }
    if (prjname === ""){
        alert("Project Name missing");
        $( "#prjname").focus(); 
        return "";
    }
    if (asnto === '') {
        alert("Assigned to missing");
        $("#asnto").focus();
        return "";
    }
    if (asndate === '') {
        alert("Assignment date missing");
        $("#asndate").focus();
        return "";
    }
    if (dl === '') {
        alert("Deadline missing");
        $("#dl").focus();
        return "";
    }

    var jsonStrObj = {
        id: id,
        name: prjname,
        assigned_to: asnto,
        assign_date: asndate,
        deadline: dl,
    };
    return JSON.stringify(jsonStrObj);
}
