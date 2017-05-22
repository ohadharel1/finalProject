
var Obj = document.getElementById("tblDrone"); //any element to be fully replaced
if(Obj.outerHTML) { //if outerHTML is supported
    Obj.outerHTML=str; ///it's simple replacement of whole element with contents of str var
}
else { //if outerHTML is not supported, there is a weird but crossbrowsered trick
    var tmpObj=document.createElement("div");
    tmpObj.innerHTML='<!--THIS DATA SHOULD BE REPLACED-->';
    ObjParent=Obj.parentNode; //Okey, element should be parented
    ObjParent.replaceChild(tmpObj,Obj); //here we placing our temporary data instead of our target, so we can find it then and replace it into whatever we want to replace to
    ObjParent.innerHTML=ObjParent.innerHTML.replace('<div><!--THIS DATA SHOULD BE REPLACED--></div>',str);
}
        console.log(response);
    });